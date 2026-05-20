"""Selected dates summary dialog."""

from typing import Optional

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QApplication,
    QDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


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
