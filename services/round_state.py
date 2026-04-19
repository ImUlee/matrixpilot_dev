"""
轮次状态管理服务

使用Flask-Caching替代全局变量，实现线程安全的状态管理
"""
import os
import json
from typing import Dict, Optional

from flask import current_app
from extensions import cache
from config import Config


# 缓存键名
CACHE_KEY_ROUND_TIMES = 'round_start_times'


def load_round_times_from_file() -> Dict[str, str]:
    """从文件加载轮次时间配置
    
    Returns:
        轮次时间字典 {device_id: start_time}
    """
    try:
        if os.path.exists(Config.ROUND_SETTINGS_FILE):
            with open(Config.ROUND_SETTINGS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data if isinstance(data, dict) else {}
    except Exception as e:
        try:
            current_app.logger.warning(f"读取 round_settings 失败: {e}")
        except RuntimeError:
            print(f"[RoundState] 读取 round_settings 失败: {e}")
    return {}


def save_round_times_to_file(data: Dict[str, str]) -> bool:
    """保存轮次时间配置到文件
    
    Args:
        data: 轮次时间字典
        
    Returns:
        保存成功返回True
    """
    try:
        # 原子写入：先写临时文件，再替换
        temp_file = Config.ROUND_SETTINGS_FILE + '.tmp'
        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        os.replace(temp_file, Config.ROUND_SETTINGS_FILE)
        return True
    except Exception as e:
        try:
            current_app.logger.error(f"保存 round_settings 失败: {e}")
        except RuntimeError:
            print(f"[RoundState] 保存 round_settings 失败: {e}")
        return False


def get_round_times() -> Dict[str, str]:
    """获取轮次时间配置（带缓存）
    
    优先从缓存读取，缓存未命中时从文件加载
    
    Returns:
        轮次时间字典
    """
    cached = cache.get(CACHE_KEY_ROUND_TIMES)
    if cached is not None:
        return cached
    
    # 缓存未命中，从文件加载
    data = load_round_times_from_file()
    cache.set(CACHE_KEY_ROUND_TIMES, data)
    return data


def get_round_time(device_id: str) -> Optional[str]:
    """获取单个设备的轮次开始时间
    
    Args:
        device_id: 设备ID，'GLOBAL' 表示全局时间
        
    Returns:
        轮次开始时间字符串，不存在返回None
    """
    times = get_round_times()
    return times.get(device_id)


def set_round_times(data: Dict[str, str]) -> bool:
    """设置轮次时间配置
    
    同时更新缓存和持久化到文件
    
    Args:
        data: 完整的轮次时间字典
        
    Returns:
        保存成功返回True
    """
    # 更新缓存
    cache.set(CACHE_KEY_ROUND_TIMES, data)
    
    # 持久化到文件
    return save_round_times_to_file(data)


def update_round_time(device_id: str, time_str: str) -> bool:
    """更新单个设备的轮次时间
    
    Args:
        device_id: 设备ID
        time_str: 时间字符串
        
    Returns:
        保存成功返回True
    """
    times = get_round_times()
    times[device_id] = time_str
    return set_round_times(times)


def clear_round_times() -> bool:
    """清除所有轮次时间配置
    
    Returns:
        清除成功返回True
    """
    cache.delete(CACHE_KEY_ROUND_TIMES)
    return save_round_times_to_file({})


def reset_all_to_global(time_str: str) -> bool:
    """重置所有设备为全局时间
    
    Args:
        time_str: 全局开始时间
        
    Returns:
        保存成功返回True
    """
    return set_round_times({'GLOBAL': time_str})


# ============================================================
# 兼容层：保持与旧代码的兼容性
# ============================================================

# 注意：以下属性用于向后兼容，新代码请使用函数接口
# 这里的 round_start_times 是一个惰性加载的代理

class _RoundTimesProxy:
    """轮次时间代理类
    
    提供与原全局变量兼容的访问方式
    """
    
    def __iter__(self):
        return iter(get_round_times())
    
    def __getitem__(self, key):
        return get_round_times()[key]
    
    def __contains__(self, key):
        return key in get_round_times()
    
    def get(self, key, default=None):
        return get_round_times().get(key, default)
    
    def keys(self):
        return get_round_times().keys()
    
    def values(self):
        return get_round_times().values()
    
    def items(self):
        return get_round_times().items()


# 兼容旧代码的全局变量访问
round_start_times = _RoundTimesProxy()


def save_round_times(data: Dict[str, str]) -> bool:
    """保存轮次时间（兼容旧接口）
    
    Args:
        data: 轮次时间字典
        
    Returns:
        保存成功返回True
    """
    return set_round_times(data)
