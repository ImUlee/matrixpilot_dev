"""
统一通知服务

整合所有Bark推送逻辑，消除重复代码
"""
import urllib.parse
import threading
from typing import Optional, List, Tuple
import requests

from constants import BarkSound, BarkGroup


class BarkNotifier:
    """Bark通知发送器
    
    封装Bark API调用，支持同步和异步发送
    
    Attributes:
        base_url: Bark服务器基础URL
        icon: 默认图标URL
    """
    
    def __init__(self, bark_url: str, icon: str = ""):
        """初始化通知器
        
        Args:
            bark_url: Bark服务器URL (如: https://api.day.app/YOUR_KEY)
            icon: 默认图标URL
        """
        self.base_url = bark_url.rstrip('/') if bark_url else None
        self.icon = icon
    
    def is_enabled(self) -> bool:
        """检查是否启用Bark通知
        
        Returns:
            配置了有效的Bark URL返回True
        """
        return bool(self.base_url)
    
    def send(
        self,
        title: str,
        body: str,
        sound: str = BarkSound.MINUET.value,
        icon: Optional[str] = None
    ) -> bool:
        """发送Bark通知
        
        Args:
            title: 通知标题
            body: 通知内容
            sound: 音效类型 (默认: minuet)
            icon: 自定义图标URL (可选，覆盖默认图标)
            
        Returns:
            发送成功返回True
            
        Examples:
            >>> notifier = BarkNotifier("https://api.day.app/key")
            >>> notifier.send("测试标题", "测试内容")
            True
        """
        if not self.is_enabled():
            return False
        
        # URL编码
        t_enc = urllib.parse.quote(title, safe='')
        b_enc = urllib.parse.quote(body, safe='')
        api_url = f"{self.base_url}/{t_enc}/{b_enc}"
        
        # 构建参数
        params = {
            "sound": sound,
            "group": BarkGroup.MAIN.value,
            "isArchive": "1"
        }
        
        # 设置图标
        final_icon = icon or self.icon
        if final_icon:
            params["icon"] = final_icon
        
        try:
            response = requests.get(api_url, params=params, timeout=10)
            return response.status_code == 200
        except Exception as e:
            print(f"[Bark Error] 通知发送失败: {e}")
            return False
    
    def send_async(self, title: str, body: str, **kwargs) -> None:
        """异步发送通知
        
        在后台线程中发送，不阻塞主线程
        
        Args:
            title: 通知标题
            body: 通知内容
            **kwargs: 传递给send()的其他参数
        """
        threading.Thread(
            target=self.send,
            args=(title, body),
            kwargs=kwargs,
            daemon=True
        ).start()


class RoundNotifier:
    """轮次提醒通知器
    
    专门处理轮次预计时间提醒
    """
    
    def __init__(self, notifier: BarkNotifier, title_template: str, body_template: str):
        """初始化轮次通知器
        
        Args:
            notifier: Bark通知器实例
            title_template: 标题模板 (支持 {group} 和 {time} 占位符)
            body_template: 内容模板 (支持 {group} 和 {time} 占位符)
        """
        self.notifier = notifier
        self.title_template = title_template
        self.body_template = body_template
    
    def notify_round(self, group_name: str, next_time: str) -> bool:
        """发送轮次提醒
        
        Args:
            group_name: 分组名称
            next_time: 预计时间字符串
            
        Returns:
            发送成功返回True
        """
        title = self.title_template.replace("{group}", group_name).replace("{time}", next_time)
        body = self.body_template.replace("{group}", group_name).replace("{time}", next_time)
        
        return self.notifier.send(title, body, sound=BarkSound.MINUET.value)


class PhysicalDropNotifier:
    """实物掉落通知器
    
    处理极品实物掉落的即时通知
    """
    
    def __init__(
        self, 
        notifier: BarkNotifier,
        title_template: str = "🎁 实物掉落提醒",
        body_template: str = "【{nickname}】抽中 {item} x{quantity}"
    ):
        """初始化实物通知器
        
        Args:
            notifier: Bark通知器实例
            title_template: 标题模板 (支持 {nickname}, {item}, {quantity} 占位符)
            body_template: 内容模板 (支持 {nickname}, {item}, {quantity} 占位符)
        """
        self.notifier = notifier
        self.title_template = title_template
        self.body_template = body_template
    
    def notify_drop(self, nickname: str, item: str, quantity: int) -> bool:
        """发送实物掉落通知
        
        Args:
            nickname: 账号昵称
            item: 物品名称
            quantity: 数量
            
        Returns:
            发送成功返回True
        """
        title = self.title_template.replace("{nickname}", nickname).replace("{item}", item).replace("{quantity}", str(quantity))
        body = self.body_template.replace("{nickname}", nickname).replace("{item}", item).replace("{quantity}", str(quantity))
        
        return self.notifier.send(title, body, sound=BarkSound.GLASS.value)
    
    def notify_batch(self, drops: List[Tuple[str, str, int]]) -> None:
        """批量发送实物掉落通知
        
        在后台线程中逐个发送
        
        Args:
            drops: 掉落列表 [(nickname, item, quantity), ...]
        """
        def send_all():
            for nickname, item, qty in drops:
                self.notify_drop(nickname, item, qty)
        
        threading.Thread(target=send_all, daemon=True).start()
