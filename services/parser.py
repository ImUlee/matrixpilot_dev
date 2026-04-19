"""
日志解析服务

处理多种格式的日志文件解析
"""
import re
from typing import List, Tuple, Optional, Any

from utils import parse_log_date
from services.db_utils import get_lp_db
from services.notifier import PhysicalDropNotifier, BarkNotifier
from constants import ItemType, DeviceStatus


# 类型别名
ParserConfig = dict
DbCursor = Any
ParseResult = Tuple[int, Optional[ParserConfig], List[Tuple]]


def _get_parser_strictness(parser: ParserConfig) -> int:
    """获取解析器严格程度
    
    用于排序解析器，优先使用更严格的解析器
    
    Args:
        parser: 解析器配置
        
    Returns:
        严格程度值（越大越严格）
    """
    if parser.get('mode') == 'split':
        return parser.get('exact_len') or max(
            int(parser.get('time_idx', 0)),
            int(parser.get('nick_idx', 1)),
            int(parser.get('val_idx', 2))
        )
    return len(parser.get('pattern', ''))


def _normalize_item_type(item_type: str) -> str:
    """标准化物品类型
    
    包含"钻"字的物品统一识别为钻石
    
    Args:
        item_type: 原始物品类型
        
    Returns:
        标准化后的物品类型
    """
    if '钻' in item_type:
        return ItemType.DIAMOND.value
    return item_type


def _parse_quantity(qty_str: str, default: int = 1) -> int:
    """解析数量字符串
    
    Args:
        qty_str: 数量字符串
        default: 默认值
        
    Returns:
        解析后的数量
    """
    qty_str = qty_str.strip()
    if qty_str.isdigit():
        return int(qty_str)
    # 尝试提取数字
    match = re.search(r'\d+', qty_str)
    return int(match.group()) if match else default


def _parse_split_mode(
    line: str, 
    parser: ParserConfig
) -> Optional[Tuple[str, str, Optional[str], Optional[str], Optional[int]]]:
    """解析分隔符模式的日志行
    
    Args:
        line: 日志行
        parser: 解析器配置
        
    Returns:
        (时间, 昵称, 原始值, 物品类型, 数量) 或 None
    """
    sep = parser.get('separator', '----')
    if not sep or sep not in line:
        return None
    
    parts = line.split(sep)
    
    # 获取映射索引
    t_idx = int(parser.get('time_idx', 0))
    n_idx = int(parser.get('nick_idx', 1))
    v_idx = int(parser.get('val_idx', -1))
    item_idx = int(parser.get('item_idx', -1))
    qty_idx = int(parser.get('qty_idx', -1))
    
    # 检查字段数量
    max_idx = max(t_idx, n_idx, v_idx, item_idx, qty_idx)
    exact_len = parser.get('exact_len')
    
    if exact_len and exact_len > 0:
        if len(parts) != exact_len:
            return None
    elif len(parts) <= max_idx:
        return None
    
    log_time_raw = parts[t_idx].strip()
    nick = parts[n_idx].strip()
    raw_val = None
    final_item_type = None
    quantity = None
    
    # 合并列模式（老版本）
    if v_idx != -1:
        raw_val = parts[v_idx].strip()
    # 分离列模式（精确识别）
    elif item_idx != -1 and qty_idx != -1:
        final_item_type = _normalize_item_type(parts[item_idx].strip())
        quantity = _parse_quantity(parts[qty_idx].strip())
    
    return log_time_raw, nick, raw_val, final_item_type, quantity


def _parse_regex_mode(
    line: str, 
    parser: ParserConfig
) -> Optional[Tuple[str, str, Optional[str], Optional[str], Optional[int]]]:
    """解析正则模式的日志行
    
    Args:
        line: 日志行
        parser: 解析器配置
        
    Returns:
        (时间, 昵称, 原始值, 物品类型, 数量) 或 None
    """
    pattern = parser.get('pattern', '')
    if not pattern:
        return None
    
    match = re.search(pattern, line)
    if not match:
        return None
    
    groups = match.groups()
    if len(groups) < 2:
        return None
    
    log_time_raw = groups[0].strip()
    nick = groups[1].strip()
    raw_val = None
    final_item_type = None
    quantity = None
    
    if len(groups) >= 4:
        final_item_type = _normalize_item_type(groups[2].strip())
        quantity = _parse_quantity(groups[3].strip())
    elif len(groups) >= 3:
        raw_val = groups[2].strip()
    
    return log_time_raw, nick, raw_val, final_item_type, quantity


def _process_raw_value(
    raw_val: str, 
    default_item_type: str
) -> Tuple[str, int]:
    """处理原始值字段
    
    当使用合并列模式时，需要从值中提取物品类型和数量
    
    Args:
        raw_val: 原始值字符串
        default_item_type: 默认物品类型
        
    Returns:
        (物品类型, 数量)
    """
    if '钻' in raw_val:
        q_match = re.search(r'\d+', raw_val)
        quantity = int(q_match.group()) if q_match else 1
        return ItemType.DIAMOND.value, quantity
    
    if raw_val.isdigit():
        return default_item_type, int(raw_val)
    
    return raw_val, 1


def parse_file_content(
    lines: List[str],
    all_parsers: List[ParserConfig],
    device_id: str,
    cursor: DbCursor
) -> ParseResult:
    """解析文件内容
    
    使用配置的解析器解析日志行，返回待插入的数据
    
    Args:
        lines: 日志行列表
        all_parsers: 解析器配置列表
        device_id: 设备ID
        cursor: 数据库游标
        
    Returns:
        Tuple[int, Optional[ParserConfig], List[Tuple]]:
            - new_count: 新增记录数
            - matched_parser: 匹配到的解析器（用于状态更新）
            - new_physicals: 新的实物掉落列表
    """
    # 按严格程度排序
    all_parsers = sorted(all_parsers, key=_get_parser_strictness, reverse=True)
    
    logs_to_insert = []
    matched_any_parser = None
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        for parser in all_parsers:
            try:
                log_time_raw = None
                nick = None
                raw_val = None
                final_item_type = None
                quantity = None
                
                # 根据模式解析
                mode = parser.get('mode', 'split')
                if mode == 'split':
                    result = _parse_split_mode(line, parser)
                else:
                    result = _parse_regex_mode(line, parser)
                
                if result is None:
                    continue
                
                log_time_raw, nick, raw_val, final_item_type, quantity = result
                
                # 验证必要字段
                if not log_time_raw or not nick:
                    continue
                
                # 解析日期
                dt = parse_log_date(log_time_raw)
                if not dt:
                    continue
                
                log_time = dt.strftime('%Y-%m-%d %H:%M:%S')
                item_type = parser.get('item_type', ItemType.DIAMOND.value)
                
                # 处理原始值
                if raw_val is not None:
                    final_item_type, quantity = _process_raw_value(raw_val, item_type)
                
                # 确保数量有效
                if quantity is None:
                    quantity = 1
                if final_item_type is None:
                    final_item_type = item_type
                
                # 生成唯一标识
                unique_sign = f"{log_time}_{nick}_{final_item_type}_{quantity}"
                
                logs_to_insert.append((
                    log_time, nick, final_item_type, quantity,
                    unique_sign, device_id, parser['id']
                ))
                
                if not matched_any_parser:
                    matched_any_parser = parser
                
                break
                
            except Exception as e:
                print(f"[Parse Error] 行解析异常跳过: {e}")
    
    # 筛选实物掉落
    physicals = [
        log for log in logs_to_insert 
        if ItemType.is_physical(log[2])
    ]
    
    # 检查是否为新实物（去重）
    new_physicals = []
    if physicals:
        placeholders = ','.join(['?'] * len(physicals))
        cursor.execute(
            f"SELECT unique_sign FROM logs WHERE unique_sign IN ({placeholders})",
            [p[4] for p in physicals]
        )
        existing_signs = set(row[0] for row in cursor.fetchall())
        new_physicals = [p for p in physicals if p[4] not in existing_signs]
    
    # 批量插入
    new_count = 0
    if logs_to_insert:
        try:
            cursor.executemany(
                "INSERT OR IGNORE INTO logs "
                "(log_time, nickname, item_type, quantity, unique_sign, device_id, template_id) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                logs_to_insert
            )
            new_count = cursor.rowcount
        except Exception as e:
            print(f"[DB Execute Error] 批量插入日志失败: {e}")
    
    return new_count, matched_any_parser, new_physicals


def process_unparsed_logs(all_parsers: List[ParserConfig], settings: Any) -> None:
    """处理未解析的日志
    
    尝试用新解析器处理隔离区中的日志
    
    Args:
        all_parsers: 解析器配置列表
        settings: 设置对象
    """
    if not all_parsers:
        return
    
    conn = get_lp_db()
    cursor = conn.cursor()
    
    # 获取未解析日志
    cursor.execute("SELECT id, device_id, raw_content FROM unparsed_logs")
    rows = cursor.fetchall()
    
    if not rows:
        cursor.execute(
            f"UPDATE devices SET last_msg = ? WHERE last_msg = ?",
            (DeviceStatus.NORMAL.value, DeviceStatus.UNRECOGNIZED.value)
        )
        conn.commit()
        return
    
    # 创建通知器
    notifier = PhysicalDropNotifier(
        BarkNotifier(settings.bark_url, settings.bark_icon)
    ) if settings and settings.bark_url and getattr(settings, 'bark_enabled', False) and settings.bark_notify_physical else None
    
    # 逐条处理
    for row in rows:
        lines = row['raw_content'].split('\n')
        new_count, matched_parser, new_physicals = parse_file_content(
            lines, all_parsers, row['device_id'], cursor
        )
        
        if matched_parser:
            # 解析成功：删除隔离记录，更新状态
            cursor.execute("DELETE FROM unparsed_logs WHERE id = ?", (row['id'],))
            cursor.execute(
                "UPDATE devices SET last_msg = ? WHERE device_id = ?",
                (DeviceStatus.NORMAL.value, row['device_id'])
            )
            
            # 发送实物通知
            if notifier and new_physicals:
                notifier.notify_batch([
                    (p[1], p[2], p[3]) for p in new_physicals
                ])
        else:
            # 解析失败：更新状态
            cursor.execute(
                "UPDATE devices SET last_msg = ? WHERE device_id = ?",
                (DeviceStatus.UNRECOGNIZED.value, row['device_id'])
            )
    
    conn.commit()
