"""Attendance statistics dialog."""

from typing import Optional

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QDialog,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class AttendanceStatsDialog(QDialog):
    """当月出勤统计对话框"""

    def __init__(
        self,
        year: int,
        month: int,
        attendance_days: int,
        overtime_days: int,
        overtime_dates: list[str],
        business_trip_days: int,
        parent: Optional[QWidget] = None,
    ) -> None:
        super().__init__(parent)
        self.setWindowTitle("当月出勤统计")
        self.setMinimumSize(420, 300)
        self._setup_ui(
            year,
            month,
            attendance_days,
            overtime_days,
            overtime_dates,
            business_trip_days,
        )

    def _setup_ui(
        self,
        year: int,
        month: int,
        attendance_days: int,
        overtime_days: int,
        overtime_dates: list[str],
        business_trip_days: int,
    ) -> None:
        layout = QVBoxLayout()
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        title_label = QLabel(f"{year}年{month}月出勤统计")
        title_label.setFont(QFont("Microsoft YaHei UI", 14, QFont.Bold))
        layout.addWidget(title_label)

        stats_group = QGroupBox("统计结果")
        stats_layout = QFormLayout()
        stats_layout.setContentsMargins(12, 20, 12, 12)
        stats_layout.setSpacing(12)

        stats_layout.addRow("出勤天数:", QLabel(f"{attendance_days} 天"))
        stats_layout.addRow("加班天数:", QLabel(f"{overtime_days} 天"))
        stats_layout.addRow("出差天数:", QLabel(f"{business_trip_days} 天"))

        overtime_text = "、".join(overtime_dates) if overtime_dates else "无"
        overtime_label = QLabel(overtime_text)
        overtime_label.setWordWrap(True)
        stats_layout.addRow("加班日期:", overtime_label)

        stats_group.setLayout(stats_layout)
        layout.addWidget(stats_group)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        close_button = QPushButton("关闭")
        close_button.clicked.connect(self.accept)
        button_layout.addWidget(close_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)
