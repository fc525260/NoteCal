"""Application settings dialog."""

from typing import Dict, Optional

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QGroupBox,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from src.theme import ThemeManager

from .log_viewer_dialog import LogViewerDialog


class SettingsDialog(QDialog):
    """设置对话框

    提供应用程序设置界面，支持主题切换、托盘设置、农历显示等选项。
    """

    def __init__(
        self,
        settings: Dict,
        parent: Optional[QWidget] = None,
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
