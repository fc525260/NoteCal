"""
日历核心模块

提供日历相关的核心功能，包括月份日历生成、日期导航和农历转换等功能。
使用 calendar.monthrange 简化天数计算。
"""
import calendar as cal_module
from datetime import datetime
from typing import Optional

from .lunar_utils import LunarUtils


class CalendarCore:
    """日历核心类

    提供日期计算、月份导航和日期格式化等核心日历功能。
    """

    def __init__(self) -> None:
        """初始化日历核心"""
        self.lunar_utils = LunarUtils()

    def get_month_calendar(self, year: int, month: int) -> list[list[int]]:
        """生成指定年月的日历数据

        创建一个 6x7 的二维数组，表示指定月份的日历网格，其中 0 表示空日期。
        使用 calendar.monthrange 简化计算。

        Args:
            year: 年份 (如 2023)
            month: 月份 (1-12)

        Returns:
            6行7列的日历数据，每行代表一周
        """
        first_weekday, days_in_month = cal_module.monthrange(year, month)

        weekday = first_weekday % 7

        calendar_data: list[list[int]] = []
        day = 1

        for _ in range(6):
            week_list: list[int] = []
            for i in range(7):
                if i < weekday:
                    week_list.append(0)
                elif day > days_in_month:
                    week_list.append(0)
                else:
                    week_list.append(day)
                    day += 1
            calendar_data.append(week_list)

            if day > days_in_month:
                while len(calendar_data) < 6:
                    calendar_data.append([0] * 7)
                break

            weekday = 0

        return calendar_data

    def navigate_month(self, year: int, month: int, delta: int) -> tuple[int, int]:
        """切换月份

        Args:
            year: 当前年份
            month: 当前月份
        delta: 偏移量 (-1 上一月, +1 下一月)

        Returns:
            (新年份, 新月份) 元组
        """
        new_month = month + delta
        new_year = year

        if new_month > 12:
            new_month = 1
            new_year += 1
        elif new_month < 1:
            new_month = 12
            new_year -= 1

        return new_year, new_month

    def is_today(self, year: int, month: int, day: int) -> bool:
        """判断给定日期是否为今天

        Args:
            year: 年份
            month: 月份
            day: 日期

        Returns:
            是否为今天
        """
        today = datetime.now()
        return year == today.year and month == today.month and day == today.day

    def get_date_string(self, year: int, month: int, day: int) -> str:
        """获取日期的字符串表示

        Args:
            year: 年份
            month: 月份
            day: 日期

        Returns:
            格式化的日期字符串 (YYYY-MM-DD)
        """
        return f"{year:04d}-{month:02d}-{day:02d}"

    def get_lunar_date_string(self, year: int, month: int, day: int) -> Optional[str]:
        """获取农历日期字符串

        Args:
            year: 年份
            month: 月份
            day: 日期

        Returns:
            农历日期字符串，若不可用则返回 None
        """
        if self.lunar_utils.is_available():
            return self.lunar_utils.get_lunar_date(year, month, day)
        return None