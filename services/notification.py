"""
实物通知服务

处理实物掉落的即时推送
"""
from typing import List, Tuple, Any

from services.notifier import BarkNotifier, PhysicalDropNotifier


def trigger_physical_notifications(
    new_physicals: List[Tuple], 
    settings: Any
) -> None:
    """触发实物掉落通知
    
    当检测到新的实物掉落时，异步发送Bark通知
    
    Args:
        new_physicals: 新实物列表 [(log_time, nickname, item_type, quantity), ...]
        settings: 设置对象
        
    Note:
        此函数为兼容接口，内部使用新的统一通知服务
    """
    # 检查是否启用
    if not new_physicals:
        return
    if not settings:
        return
    if not getattr(settings, 'bark_enabled', False):
        return
    if not settings.bark_url:
        return
    if not settings.bark_notify_physical:
        return
    
    # 获取实物推送配置
    physical_title = getattr(settings, 'bark_physical_title', '🎁 实物掉落提醒')
    physical_body = getattr(settings, 'bark_physical_body', '【{nickname}】抽中 {item} x{quantity}')
    
    # 创建通知器并发送
    bark_notifier = BarkNotifier(settings.bark_url, settings.bark_icon or "")
    physical_notifier = PhysicalDropNotifier(
        bark_notifier, 
        title_template=physical_title,
        body_template=physical_body
    )
    
    # 转换数据格式并批量发送
    drops = [(p[1], p[2], p[3]) for p in new_physicals]
    physical_notifier.notify_batch(drops)
