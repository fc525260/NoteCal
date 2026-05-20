"""Year and month selection dialog."""

from typing import Optional

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QHBoxLayout,
    QLabel,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)


class YearMonthDialog(QDialog):
    """年月选择对话框

    提供可视化的年月选择界面。
    """

    def __init__(
        self,
        current_year: int,
        current_month: int,
        parent: Optional[QWidget] = None,
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
            "七月", "八月", "九月", "十月", "十一月", "十二月",
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
