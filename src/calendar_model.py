"""
日历模型模块

提供基于 QAbstractTableModel 的日历数据模型，用于 QTableView 显示。
"""
from typing import Dict, Any, Optional
from PyQt5.QtCore import QAbstractTableModel, Qt, QModelIndex
from PyQt5.QtGui import QColor

from .calendar_core import CalendarCore
from .data_manager import DataManager


class CalendarModel(QAbstractTableModel):
    """日历模型类

    使用 TableModel 模式提供日历数据，支持自定义角色传递日期信息。
    """

    ROLE_DAY = Qt.UserRole + 1
    ROLE_YEAR = Qt.UserRole + 2
    ROLE_MONTH = Qt.UserRole + 3
    ROLE_DATE_STRING = Qt.UserRole + 4
    ROLE_IS_TODAY = Qt.UserRole + 5
    ROLE_HAS_NOTE = Qt.UserRole + 6
    ROLE_LUNAR = Qt.UserRole + 7
    ROLE_OVERTIME = Qt.UserRole + 8
    ROLE_BUSINESS_TRIP = Qt.UserRole + 9
    ROLE_IS_MARKED = Qt.UserRole + 10

    WEEKDAYS = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]

    def __init__(
        self,
        calendar_core: CalendarCore,
        data_manager: DataManager,
        parent=None
    ) -> None:
        """初始化日历模型

        Args:
            calendar_core: 日历核心实例
            data_manager: 数据管理器实例
            parent: 父对象
        """
        super().__init__(parent)
        self._calendar_core = calendar_core
        self._data_manager = data_manager

        self._year: int = 0
        self._month: int = 0
        self._calendar_data: list[list[int]] = []
        self._marked_dates: set[str] = set()

    @property
    def year(self) -> int:
        return self._year

    @property
    def month(self) -> int:
        return self._month

    def set_date(self, year: int, month: int) -> None:
        """设置显示的年月

        Args:
            year: 年份
            month: 月份 (1-12)
        """
        if self._year == year and self._month == month:
            return

        self.beginResetModel()
        self._year = year
        self._month = month
        self._calendar_data = self._calendar_core.get_month_calendar(year, month)
        self.endResetModel()

    def refresh(self) -> None:
        """刷新数据"""
        self.dataChanged.emit(self.index(0, 0), self.index(5, 6))

    def set_marked_dates(self, date_strings: set[str]) -> None:
        """设置需要高亮标记的日期"""
        self._marked_dates = set(date_strings)
        self.refresh()

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        """返回行数（日历固定 6 行）"""
        return 6

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        """返回列数（固定 7 列）"""
        return 7

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole) -> Any:
        """获取指定索引的数据

        Args:
            index: 模型索引
            role: 角色标识

        Returns:
            对应角色的数据
        """
        if not index.isValid():
            return None

        row = index.row()
        col = index.column()

        if row >= len(self._calendar_data) or col >= 7:
            return None

        day = self._calendar_data[row][col]

        if day == 0:
            return None

        year = self._year
        month = self._month

        if role == Qt.DisplayRole:
            return str(day)

        if role == Qt.FontRole:
            return None

        if role == Qt.TextAlignmentRole:
            return Qt.AlignCenter

        if role == self.ROLE_DAY:
            return day

        if role == self.ROLE_YEAR:
            return year

        if role == self.ROLE_MONTH:
            return month

        if role == self.ROLE_DATE_STRING:
            return self._calendar_core.get_date_string(year, month, day)

        if role == self.ROLE_IS_TODAY:
            return self._calendar_core.is_today(year, month, day)

        if role == self.ROLE_HAS_NOTE:
            date_str = self._calendar_core.get_date_string(year, month, day)
            content, _, _ = self._data_manager.get_note(date_str)
            return bool(content)

        if role == self.ROLE_OVERTIME:
            date_str = self._calendar_core.get_date_string(year, month, day)
            _, is_overtime, _ = self._data_manager.get_note(date_str)
            return is_overtime

        if role == self.ROLE_BUSINESS_TRIP:
            date_str = self._calendar_core.get_date_string(year, month, day)
            _, _, is_business_trip = self._data_manager.get_note(date_str)
            return is_business_trip

        if role == self.ROLE_IS_MARKED:
            date_str = self._calendar_core.get_date_string(year, month, day)
            return date_str in self._marked_dates

        if role == self.ROLE_LUNAR:
            if self._data_manager.get_setting("show_lunar", True):
                return self._calendar_core.get_lunar_date_string(year, month, day)
            return None

        return None

    def headerData(
        self,
        section: int,
        orientation: Qt.Orientation,
        role: int = Qt.DisplayRole
    ) -> Any:
        """获取表头数据

        Args:
            section: 索引
            orientation: 方向
            role: 角色

        Returns:
            表头数据
        """
        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:
            if 0 <= section < len(self.WEEKDAYS):
                return self.WEEKDAYS[section]
            return None

        if orientation == Qt.Vertical:
            return None

        return None

    def get_date_info(self, row: int, col: int) -> Optional[Dict[str, Any]]:
        """获取指定行列的日期信息

        Args:
            row: 行索引 (0-5)
            col: 列索引 (0-6)

        Returns:
            日期信息字典，无效日期返回 None
        """
        if row >= len(self._calendar_data) or col >= 7:
            return None

        day = self._calendar_data[row][col]
        if day == 0:
            return None

        date_str = self._calendar_core.get_date_string(self._year, self._month, day)
        lunar = None
        if self._data_manager.get_setting("show_lunar", True):
            lunar = self._calendar_core.get_lunar_date_string(self._year, self._month, day)

        content, is_overtime, is_business_trip = self._data_manager.get_note(date_str)
        return {
            "day": day,
            "year": self._year,
            "month": self._month,
            "date_string": date_str,
            "is_today": self._calendar_core.is_today(self._year, self._month, day),
            "has_note": bool(content),
            "overtime": is_overtime,
            "business_trip": is_business_trip,
            "lunar": lunar,
        }
