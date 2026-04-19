"""
类型定义模块

集中管理项目中的类型提示，提高代码可读性和IDE支持
"""
from typing import TypedDict, List, Optional, Dict, Any
from datetime import datetime


class ParserConfig(TypedDict, total=False):
    """解析器配置
    
    Attributes:
        id: 解析器唯一标识
        name: 解析器名称
        mode: 解析模式 ('split' | 'regex')
        item_type: 默认物品类型
        separator: 分隔符 (split模式)
        pattern: 正则表达式 (regex模式)
        time_idx: 时间字段索引
        nick_idx: 昵称字段索引
        val_idx: 值字段索引 (旧版兼容)
        item_idx: 物品字段索引
        qty_idx: 数量字段索引
        exact_len: 期望字段数量
    """
    id: str
    name: str
    mode: str
    item_type: str
    separator: Optional[str]
    pattern: Optional[str]
    time_idx: int
    nick_idx: int
    val_idx: int
    item_idx: int
    qty_idx: int
    exact_len: Optional[int]


class LogEntry(TypedDict):
    """日志条目
    
    Attributes:
        log_time: 日志时间 (格式: YYYY-MM-DD HH:MM:SS)
        nickname: 账号昵称
        item_type: 物品类型
        quantity: 数量
        unique_sign: 唯一标识 (用于去重)
        device_id: 设备ID
        template_id: 模板ID
    """
    log_time: str
    nickname: str
    item_type: str
    quantity: int
    unique_sign: str
    device_id: str
    template_id: str


class NodeInfo(TypedDict):
    """节点信息
    
    Attributes:
        device_id: 设备唯一标识
        nickname: 节点昵称
        log_count: 日志总数
        last_log_time: 最后日志时间
        is_active: 是否在线
    """
    device_id: str
    nickname: str
    log_count: int
    last_log_time: str
    is_active: bool


class SettingsDict(TypedDict):
    """设置字典
    
    用于API返回的设置数据结构
    """
    interval_hours: int
    bark_url: str
    bark_title: str
    bark_body: str
    bark_icon: str
    bark_notify_physical: bool
    faq_json: str
    parsers_json: str


class RecordData(TypedDict):
    """记录数据
    
    存储在Record.data JSON字段中的数据结构
    """
    # 动态结构，key为分组名，value为统计数据
    pass


class ApiResponse(TypedDict, total=False):
    """通用API响应
    
    Attributes:
        status: 状态 ('success' | 'error')
        message: 消息文本
        data: 响应数据
    """
    status: str
    message: str
    data: Dict[str, Any]


# ==================== 函数类型别名 ====================

# 数据库游标类型 (兼容sqlite3.Cursor)
DbCursor = Any

# 数据库连接类型 (兼容sqlite3.Connection)
DbConnection = Any

# 物理掉落数据: (log_time, nickname, item_type, quantity)
PhysicalDrop = tuple[str, str, str, int]

# 解析结果: (new_count, matched_parser, new_physicals)
ParseResult = tuple[int, Optional[ParserConfig], List[PhysicalDrop]]
