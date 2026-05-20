"""Date note editing dialog."""

from typing import Optional

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QCheckBox,
    QDialog,
    QDialogButtonBox,
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


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
        parent: Optional[QWidget] = None,
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
            QSizePolicy.Expanding,
        )

        self._setup_ui(date_str, content, overtime, business_trip)

    def _setup_ui(
        self,
        date_str: str,
        content: str,
        overtime: bool,
        business_trip: bool,
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
