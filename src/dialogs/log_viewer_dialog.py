"""Application log viewer dialog."""

import os
import sys
from typing import Optional

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from src.theme import ThemeManager


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
            app_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        log_dir = os.path.join(app_dir, "data")
        log_file = os.path.join(log_dir, "notecal.log")

        if not os.path.exists(log_file):
            return "日志文件不存在。\n\n日志将在程序运行时自动生成。"

        try:
            with open(log_file, encoding="utf-8") as f:
                lines = f.readlines()

            recent_lines = lines[-max_lines:] if len(lines) > max_lines else lines
            return "".join(recent_lines)
        except Exception as e:
            return f"读取日志失败: {e}"
