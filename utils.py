"""
工具函数模块

提供日期解析、格式化等通用功能
"""
import re
from datetime import datetime
from typing import Optional, List

from constants import Defaults


# ============================================================
# 月份映射表
# ============================================================
MONTH_MAP = {
    'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4,
    'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8,
    'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
}


# ============================================================
# 日期参数格式化
# ============================================================
def format_datetime_param(dt_str: str, is_end: bool = False) -> str:
    """格式化日期时间参数
    
    将各种格式的日期字符串转换为标准格式
    
    Args:
        dt_str: 输入日期字符串
        is_end: 是否为结束时间（补23:59:59）
        
    Returns:
        格式化后的日期时间字符串
        
    Examples:
        >>> format_datetime_param("2024-01-15")
        "2024-01-15 00:00:00"
        >>> format_datetime_param("2024-01-15", is_end=True)
        "2024-01-15 23:59:59"
        >>> format_datetime_param("")
        "2000-01-01 00:00:00"
    """
    if not dt_str:
        return Defaults.DATE_MAX if is_end else Defaults.DATE_MIN
    
    dt_str = dt_str.replace('T', ' ')
    
    # 仅日期：补全时间
    if len(dt_str) == 10:
        suffix = "23:59:59" if is_end else "00:00:00"
        return f"{dt_str} {suffix}"
    
    # 日期+小时分钟：补全秒
    if len(dt_str) == 16:
        suffix = "59" if is_end else "00"
        return f"{dt_str}:{suffix}"
    
    return dt_str


# ============================================================
# 日期解析器类
# ============================================================
class DateParser:
    """日期解析器
    
    支持多种日期格式的智能解析
    """
    
    @staticmethod
    def parse_english_format(date_str: str) -> Optional[datetime]:
        """解析英文月份格式
        
        支持格式: 15/Jan/2024 10:30:00
        
        Args:
            date_str: 日期字符串
            
        Returns:
            解析成功的datetime对象，失败返回None
        """
        if '/' not in date_str or not re.search(r'[a-zA-Z]', date_str):
            return None
        
        parts = date_str.split()
        if len(parts) < 1:
            return None
        
        d_parts = parts[0].split('/')
        if len(d_parts) < 3:
            return None
        
        # 解析月份
        month = MONTH_MAP.get(d_parts[1])
        if not month:
            return None
        
        try:
            day = int(d_parts[0])
            year = int(d_parts[2])
        except ValueError:
            return None
        
        # 解析时间部分
        hour, minute, second = 0, 0, 0
        if len(parts) > 1:
            t_parts = parts[1].split(':')
            try:
                hour = int(t_parts[0]) if len(t_parts) > 0 else 0
                minute = int(t_parts[1]) if len(t_parts) > 1 else 0
                second = int(t_parts[2]) if len(t_parts) > 2 else 0
            except ValueError:
                pass
        
        try:
            return datetime(year, month, day, hour, minute, second)
        except ValueError:
            return None
    
    @staticmethod
    def parse_numeric_format(nums: List[int], current_year: int) -> Optional[datetime]:
        """解析纯数字格式
        
        支持格式:
        - 2024, 1, 15, 10, 30, 0 (年月日时分秒)
        - 24, 1, 15, 10, 30, 0 (两位年)
        - 1, 15, 10, 30 (无年份，自动补全年份)
        
        Args:
            nums: 提取的数字列表
            current_year: 当前年份（用于补全）
            
        Returns:
            解析成功的datetime对象，失败返回None
        """
        if len(nums) < 2:
            return None
        
        try:
            # 格式1: 年份开头 (2024, 1, 15, ...)
            if nums[0] > 1000:
                year = nums[0]
                month = nums[1] if len(nums) > 1 else 1
                day = nums[2] if len(nums) > 2 else 1
                hour = nums[3] if len(nums) > 3 else 0
                minute = nums[4] if len(nums) > 4 else 0
                second = nums[5] if len(nums) > 5 else 0
            
            # 格式2: 两位年开头 (24, 1, 15, ...)
            elif len(nums) >= 6 and nums[0] > 20:
                year = 2000 + nums[0]
                month, day = nums[1], nums[2]
                hour, minute, second = nums[3], nums[4], nums[5]
            
            # 格式3: 无年份 (1, 15, ...) - 使用当前年
            else:
                year = current_year
                month, day = nums[0], nums[1]
                hour = nums[2] if len(nums) > 2 else 0
                minute = nums[3] if len(nums) > 3 else 0
                second = nums[4] if len(nums) > 4 else 0
            
            # 验证日期有效性
            if not (1 <= month <= 12 and 1 <= day <= 31):
                return None
            if not (0 <= hour <= 23 and 0 <= minute <= 59 and 0 <= second <= 59):
                return None
            
            return datetime(year, month, day, hour, minute, second)
            
        except (ValueError, IndexError):
            return None


# ============================================================
# 主解析函数
# ============================================================
def parse_log_date(date_str: str) -> Optional[datetime]:
    """解析多种格式的日期字符串
    
    支持格式:
        - 英文月份: 15/Jan/2024 10:30:00
        - 标准格式: 2024-01-15 10:30:00
        - 斜杠格式: 2024/01/15 10:30:00
        - 简化格式: 1/15 10:30 (自动补全年份)
        
    Args:
        date_str: 待解析的日期字符串
        
    Returns:
        解析成功的datetime对象，失败返回None
        
    Examples:
        >>> parse_log_date("2024-01-15")
        datetime(2024, 1, 15, 0, 0)
        >>> parse_log_date("15/Jan/2024 10:30:00")
        datetime(2024, 1, 15, 10, 30, 0)
        >>> parse_log_date("invalid")
        None
    """
    try:
        date_str = str(date_str).strip()
        if not date_str:
            return None
        
        # 尝试英文月份格式
        result = DateParser.parse_english_format(date_str)
        if result:
            return result
        
        # 提取所有数字
        nums = list(map(int, re.findall(r'\d+', date_str)))
        if len(nums) < 2:
            return None
        
        # 解析数字格式
        return DateParser.parse_numeric_format(nums, datetime.now().year)
        
    except (ValueError, TypeError):
        return None
