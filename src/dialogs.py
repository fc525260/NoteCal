"""
对话框模块

提供应用程序中使用的各种对话框，包括笔记编辑、日期选择和设置界面。
支持浅色/深色主题。
"""
from typing import Dict, Optional
import os
import sys

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit,
    QDialogButtonBox, QComboBox, QSpinBox, QGroupBox,
    QCheckBox, QFormLayout, QWidget, QSizePolicy, QPushButton
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication

from .theme import ThemeManager


class DateNoteDialog(QDialog):
    """日期笔记对话框

    提供特定日期的笔记编辑界面，支持笔记的查看和修改。
    """

    def __init__(
        self,
        date_str: str,
        content: str,
        overtime: bool = False,
        business_trip: bool = False,
        parent: Optional[QWidget] = None
    ) -> None:
        """初始化日期笔记对话框

        Args:
            date_str: 日期字符串 (格式：YYYY-MM-DD)
            content: 初始笔记内容
            overtime: 是否加班
            business_trip: 是否出差
            parent: 父窗口
        """
        super().__init__(parent)
        self.setWindowTitle(f"笔记 - {date_str}")
        self.setMinimumSize(450, 350)
        self.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )

        self._setup_ui(date_str, content, overtime, business_trip)

    def _setup_ui(
        self,
        date_str: str,
        content: str,
        overtime: bool,
        business_trip: bool
    ) -> None:
        """设置 UI"""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        title_label = QLabel(f"📅 {date_str}")
        title_label.setFont(QFont("Microsoft YaHei UI", 14, QFont.Bold))
        title_label.setAlignment(Qt.AlignLeft)
        layout.addWidget(title_label)

        self.note_edit = QTextEdit()
        self.note_edit.setPlainText(content)
        self.note_edit.setFont(QFont("Microsoft YaHei UI", 12))
        self.note_edit.setPlaceholderText("在此输入笔记内容...")
        layout.addWidget(self.note_edit)

        options_layout = QHBoxLayout()
        options_layout.addStretch()

        self.overtime_checkbox = QCheckBox("加班")
        self.overtime_checkbox.setChecked(overtime)
        self.overtime_checkbox.setFont(QFont("Microsoft YaHei UI", 11))
        options_layout.addWidget(self.overtime_checkbox)

        self.business_trip_checkbox = QCheckBox("出差")
        self.business_trip_checkbox.setChecked(business_trip)
        self.business_trip_checkbox.setFont(QFont("Microsoft YaHei UI", 11))
        options_layout.addWidget(self.business_trip_checkbox)

        layout.addLayout(options_layout)

        button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        ok_button = button_box.button(QDialogButtonBox.Ok)
        ok_button.setText("保存")

        cancel_button = button_box.button(QDialogButtonBox.Cancel)
        cancel_button.setText("取消")

        layout.addWidget(button_box)

        self.setLayout(layout)

    def get_note_content(self) -> str:
        """获取笔记内容

        Returns:
            笔记文本内容
        """
        return self.note_edit.toPlainText()

    def is_overtime(self) -> bool:
        """获取是否加班

        Returns:
            是否加班
        """
        return self.overtime_checkbox.isChecked()

    def is_business_trip(self) -> bool:
        """获取是否出差

        Returns:
            是否出差
        """
        return self.business_trip_checkbox.isChecked()


class YearMonthDialog(QDialog):
    """年月选择对话框

    提供可视化的年月选择界面。
    """

    def __init__(
        self,
        current_year: int,
        current_month: int,
        parent: Optional[QWidget] = None
    ) -> None:
        """初始化年月选择对话框

        Args:
            current_year: 当前年份
            current_month: 当前月份
            parent: 父窗口
        """
        super().__init__(parent)
        self.setWindowTitle("选择年月")
        self.setMinimumSize(320, 220)

        self._setup_ui(current_year, current_month)

    def _setup_ui(self, current_year: int, current_month: int) -> None:
        """设置 UI"""
        layout = QVBoxLayout()
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)

        title_label = QLabel("请选择年月")
        title_label.setFont(QFont("Microsoft YaHei UI", 13, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        picker_layout = QHBoxLayout()
        picker_layout.setSpacing(16)

        self.year_spin = QSpinBox()
        self.year_spin.setRange(1900, 2100)
        self.year_spin.setValue(current_year)
        self.year_spin.setFont(QFont("Microsoft YaHei UI", 12))
        self.year_spin.setFixedWidth(100)

        year_label = QLabel("年")
        year_label.setFont(QFont("Microsoft YaHei UI", 12))

        self.month_combo = QComboBox()
        self.month_combo.setFont(QFont("Microsoft YaHei UI", 12))
        self.month_combo.addItems([
            "一月", "二月", "三月", "四月", "五月", "六月",
            "七月", "八月", "九月", "十月", "十一月", "十二月"
        ])
        self.month_combo.setCurrentIndex(current_month - 1)
        self.month_combo.setFixedWidth(100)

        month_label = QLabel("月")
        month_label.setFont(QFont("Microsoft YaHei UI", 12))

        picker_layout.addStretch()
        picker_layout.addWidget(self.year_spin)
        picker_layout.addWidget(year_label)
        picker_layout.addSpacing(16)
        picker_layout.addWidget(self.month_combo)
        picker_layout.addWidget(month_label)
        picker_layout.addStretch()

        layout.addLayout(picker_layout)

        button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        ok_button = button_box.button(QDialogButtonBox.Ok)
        ok_button.setText("确定")

        cancel_button = button_box.button(QDialogButtonBox.Cancel)
        cancel_button.setText("取消")

        layout.addWidget(button_box)

        self.setLayout(layout)

    def get_year_month(self) -> tuple[int, int]:
        """获取选择的年月

        Returns:
            (年份, 月份) 元组
        """
        return self.year_spin.value(), self.month_combo.currentIndex() + 1


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
        parent: Optional[QWidget] = None
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
            business_trip_days
        )

    def _setup_ui(
        self,
        year: int,
        month: int,
        attendance_days: int,
        overtime_days: int,
        overtime_dates: list[str],
        business_trip_days: int
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


class SelectedSummaryDialog(QDialog):
    """所选日期工作总结对话框"""

    def __init__(self, summary_text: str, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("所选日期内容")
        self.setMinimumSize(520, 360)
        self._summary_text = summary_text
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout()
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        title_label = QLabel("所选日期内容")
        title_label.setFont(QFont("Microsoft YaHei UI", 14, QFont.Bold))
        layout.addWidget(title_label)

        self.summary_edit = QTextEdit()
        self.summary_edit.setPlainText(self._summary_text)
        self.summary_edit.setFont(QFont("Microsoft YaHei UI", 11))
        self.summary_edit.setReadOnly(False)
        layout.addWidget(self.summary_edit)

        button_layout = QHBoxLayout()
        button_layout.addStretch()

        copy_button = QPushButton("一键复制")
        copy_button.clicked.connect(self._copy_summary)
        button_layout.addWidget(copy_button)

        close_button = QPushButton("关闭")
        close_button.clicked.connect(self.accept)
        button_layout.addWidget(close_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def _copy_summary(self) -> None:
        QApplication.clipboard().setText(self.summary_edit.toPlainText())


class SettingsDialog(QDialog):
    """设置对话框

    提供应用程序设置界面，支持主题切换、托盘设置、农历显示等选项。
    """

    def __init__(
        self,
        settings: Dict,
        parent: Optional[QWidget] = None
    ) -> None:
        """初始化设置对话框

        Args:
            settings: 当前设置字典
            parent: 父窗口
        """
        super().__init__(parent)
        self.setWindowTitle("设置")
        self.setMinimumSize(400, 320)

        self.settings = settings

        self._setup_ui()

    def _setup_ui(self) -> None:
        """设置 UI"""
        layout = QVBoxLayout()
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)

        title_label = QLabel("⚙️ 应用设置")
        title_label.setFont(QFont("Microsoft YaHei UI", 14, QFont.Bold))
        layout.addWidget(title_label)

        theme_group = QGroupBox("外观")
        theme_layout = QFormLayout()
        theme_layout.setContentsMargins(12, 20, 12, 12)
        theme_layout.setSpacing(12)

        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["浅色", "深色"])
        current_theme = self.settings.get("theme", "light")
        self.theme_combo.setCurrentIndex(0 if current_theme == "light" else 1)

        theme_layout.addRow("主题:", self.theme_combo)
        theme_group.setLayout(theme_layout)
        layout.addWidget(theme_group)

        tray_group = QGroupBox("系统托盘")
        tray_layout = QFormLayout()
        tray_layout.setContentsMargins(12, 20, 12, 12)
        tray_layout.setSpacing(12)

        self.minimize_to_tray_check = QCheckBox()
        self.minimize_to_tray_check.setChecked(
            self.settings.get("minimize_to_tray", True)
        )
        tray_layout.addRow("最小化到系统托盘:", self.minimize_to_tray_check)
        tray_group.setLayout(tray_layout)
        layout.addWidget(tray_group)

        calendar_group = QGroupBox("日历显示")
        calendar_layout = QFormLayout()
        calendar_layout.setContentsMargins(12, 20, 12, 12)
        calendar_layout.setSpacing(12)

        self.show_lunar_check = QCheckBox()
        self.show_lunar_check.setChecked(self.settings.get("show_lunar", True))
        calendar_layout.addRow("显示农历:", self.show_lunar_check)
        calendar_group.setLayout(calendar_layout)
        layout.addWidget(calendar_group)

        about_group = QGroupBox("关于")
        about_layout = QVBoxLayout()
        about_layout.setContentsMargins(12, 20, 12, 12)

        log_button = QPushButton("📋 查看运行日志")
        log_button.setFont(QFont("Microsoft YaHei UI", 11))
        log_button.clicked.connect(self._show_log_viewer)
        about_layout.addWidget(log_button)

        about_group.setLayout(about_layout)
        layout.addWidget(about_group)

        layout.addStretch()

        button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        ok_button = button_box.button(QDialogButtonBox.Ok)
        ok_button.setText("确定")

        cancel_button = button_box.button(QDialogButtonBox.Cancel)
        cancel_button.setText("取消")

        layout.addWidget(button_box)

        self.setLayout(layout)

    def get_settings(self) -> Dict:
        """获取设置

        Returns:
            更新后的设置字典
        """
        theme_text = self.theme_combo.currentText()
        theme_value = "light" if theme_text == "浅色" else "dark"

        return {
            "theme": theme_value,
            "minimize_to_tray": self.minimize_to_tray_check.isChecked(),
            "show_lunar": self.show_lunar_check.isChecked(),
        }

    def _show_log_viewer(self) -> None:
        """显示日志查看器"""
        dialog = LogViewerDialog(self)
        theme_manager = ThemeManager.get_instance()
        theme_manager.apply_to_widget(dialog)
        dialog.exec_()


class LogViewerDialog(QDialog):
    """日志查看对话框"""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("运行日志")
        self.setMinimumSize(600, 400)
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout()
        layout.setContentsMargins(16, 16, 16, 16)

        title_label = QLabel("📋 运行日志")
        title_label.setFont(QFont("Microsoft YaHei UI", 14, QFont.Bold))
        layout.addWidget(title_label)

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setFont(QFont("Consolas", 10))
        self._load_logs()
        layout.addWidget(self.log_text)

        button_layout = QHBoxLayout()
        button_layout.addStretch()

        refresh_button = QPushButton("刷新")
        refresh_button.clicked.connect(self._load_logs)
        button_layout.addWidget(refresh_button)

        close_button = QPushButton("关闭")
        close_button.clicked.connect(self.accept)
        button_layout.addWidget(close_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def _load_logs(self) -> None:
        theme_manager = ThemeManager.get_instance()
        is_dark = theme_manager.current_theme == ThemeManager.DARK_THEME

        log_content = self._get_recent_logs(500)

        if is_dark:
            self.log_text.setStyleSheet("background-color: #2D2D2D; color: #E0E0E0;")
        else:
            self.log_text.setStyleSheet("background-color: #FAFAFA; color: #333333;")

        self.log_text.setPlainText(log_content)

    def _get_recent_logs(self, max_lines: int = 500) -> str:
        if getattr(sys, "frozen", False):
            app_dir = os.path.dirname(sys.executable)
        else:
            app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        log_dir = os.path.join(app_dir, "data")
        log_file = os.path.join(log_dir, "notecal.log")

        if not os.path.exists(log_file):
            return "日志文件不存在。\n\n日志将在程序运行时自动生成。"

        try:
            with open(log_file, "r", encoding="utf-8") as f:
                lines = f.readlines()

            recent_lines = lines[-max_lines:] if len(lines) > max_lines else lines
            return "".join(recent_lines)
        except Exception as e:
            return f"读取日志失败: {e}"
