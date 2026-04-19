"""
MatrixPilot 常量定义模块

消除魔法字符串，统一管理业务常量
"""
from enum import Enum


class ItemType(str, Enum):
    """物品类型"""
    DIAMOND = "钻石"
    DYNAMIC = "动态"
    
    @classmethod
    def is_physical(cls, item_type: str) -> bool:
        """判断是否为实物（非钻石/动态）
        
        Args:
            item_type: 物品类型字符串
            
        Returns:
            如果是实物返回True，钻石/动态返回False
            
        Examples:
            >>> ItemType.is_physical("钻石")
            False
            >>> ItemType.is_physical("金币")
            True
        """
        return item_type not in (cls.DIAMOND.value, cls.DYNAMIC.value)


class DeviceStatus(str, Enum):
    """设备状态"""
    NORMAL = "正常"
    UNRECOGNIZED = "格式未识别"
    OFFLINE = "已离线历史节点"


class BarkSound(str, Enum):
    """Bark通知音效"""
    MINUET = "minuet"      # 常规通知
    GLASS = "glass"        # 实物掉落


class BarkGroup(str, Enum):
    """Bark通知分组"""
    MAIN = "MatrixPilot"


# ==================== API响应消息 ====================

class Message:
    """API响应消息常量"""
    
    class Node:
        """节点相关消息"""
        DELETE_SUCCESS = "🗑️ 节点已从在线列表中移除，其底层数据已安全保留。"
        INVALID_PARAM = "无效的节点参数"
    
    class History:
        """历史记录相关消息"""
        MERGE_SUCCESS = "✅ 已成功将 {old} 归并至 {new}"
        DELETE_SUCCESS = "🗑️ 已永久清除 {nickname} 的所有轨迹记录"
        INVALID_NICKNAME = "未指定目标账号"
        INVALID_NEW_NICKNAME = "目标新昵称无效"
    
    class Common:
        """通用消息"""
        SUCCESS = "success"
        ERROR = "error"


# ==================== 默认配置 ====================

class Defaults:
    """默认值常量"""
    
    # 设置默认值
    INTERVAL_HOURS = 72
    BARK_TITLE = "MatrixPilot 提醒"
    BARK_BODY = "分组【{group}】预计下轮时间已到！"
    BARK_PHYSICAL_TITLE = "🎁 实物掉落提醒"
    BARK_PHYSICAL_BODY = "【{nickname}】抽中 {item} x{quantity}"
    
    # 日期范围默认值
    DATE_MIN = "2000-01-01 00:00:00"
    DATE_MAX = "2099-12-31 23:59:59"
