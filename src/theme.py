"""
主题管理模块

提供 Win11 Fluent 风格的 QSS 样式表，支持浅色/深色模式切换。
"""
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class ThemeManager:
    """主题管理器

    管理应用的主题样式，支持浅色和深色两种模式。
    """

    LIGHT_THEME = "light"
    DARK_THEME = "dark"

    _instance: Optional["ThemeManager"] = None

    def __init__(self) -> None:
        """初始化主题管理器"""
        self._current_theme = self.LIGHT_THEME

    @classmethod
    def get_instance(cls) -> "ThemeManager":
        """获取单例实例"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @property
    def current_theme(self) -> str:
        """获取当前主题"""
        return self._current_theme

    def set_theme(self, theme: str) -> None:
        """设置主题

        Args:
            theme: 主题名称 (light/dark)
        """
        if theme in (self.LIGHT_THEME, self.DARK_THEME):
            self._current_theme = theme
            logger.info(f"主题已切换为: {theme}")
        else:
            logger.warning(f"未知主题: {theme}，使用默认浅色主题")
            self._current_theme = self.LIGHT_THEME

    def toggle_theme(self) -> str:
        """切换主题

        Returns:
            切换后的主题名称
        """
        new_theme = self.DARK_THEME if self._current_theme == self.LIGHT_THEME else self.LIGHT_THEME
        self.set_theme(new_theme)
        return new_theme

    def get_stylesheet(self) -> str:
        """获取当前主题的完整 QSS 样式表

        Returns:
            QSS 样式表字符串
        """
        if self._current_theme == self.DARK_THEME:
            return self._get_dark_theme()
        return self._get_light_theme()

    def apply_to_widget(self, widget) -> None:
        """应用主题到指定控件

        Args:
            widget: QWidget 实例
        """
        widget.setStyleSheet(self.get_stylesheet())

    @staticmethod
    def _get_light_theme() -> str:
        """获取浅色主题 QSS"""
        return """
        /* 全局 */
        QWidget {
            font-family: "Segoe UI Variable", "Segoe UI", "Microsoft YaHei UI", sans-serif;
            font-size: 15px;
        }

        /* 主窗口 */
        QMainWindow {
            background-color: #F9F9F9;
        }

        /* 标签 */
        QLabel {
            color: #202020;
            background-color: transparent;
        }

        /* 按钮 - Win11 风格 */
        QPushButton {
            background-color: rgba(249, 249, 249, 0.8);
            border: 1px solid transparent;
            border-radius: 4px;
            padding: 8px 20px;
            color: #202020;
            min-height: 32px;
            font-size: 16px;
        }

        QPushButton:hover {
            background-color: rgba(249, 249, 249, 0.95);
            border-color: rgba(0, 0, 0, 0.05);
        }

        QPushButton:pressed {
            background-color: #E5E5E5;
        }

        QPushButton:focus {
            outline: none;
            border-color: #0078D4;
        }

        QPushButton:disabled {
            background-color: transparent;
            color: #A0A0A0;
        }

        QPushButton:default {
            background-color: #0078D4;
            color: #FFFFFF;
            border: none;
        }

        QPushButton:default:hover {
            background-color: #106EBE;
        }

        QPushButton:default:pressed {
            background-color: #005A9E;
        }

/* 顶部标题区域 - Win11 风格 */
        #HeaderWidget {
            background-color: transparent;
            border-bottom: 1px solid rgba(0, 0, 0, 0.08);
        }

        /* 底部按钮栏 - Win11 风格 */
        #BottomButton {
            background-color: transparent;
            border: none;
            border-radius: 4px;
            padding: 9px 18px;
            font-size: 16px;
            color: #404040;
        }

        #BottomButton:hover {
            background-color: rgba(0, 0, 0, 0.05);
            color: #202020;
        }

        #BottomButton:pressed {
            background-color: rgba(0, 0, 0, 0.1);
        }

        /* 导航按钮 - Win11 风格 */
        #NavButton {
            background-color: transparent;
            border: none;
            border-radius: 4px;
            font-size: 20px;
            color: #404040;
            min-width: 38px;
            min-height: 38px;
            padding: 4px 8px;
        }

        #NavButton:hover {
            background-color: rgba(0, 0, 0, 0.05);
            color: #202020;
        }

        #NavButton:pressed {
            background-color: rgba(0, 0, 0, 0.1);
        }

        #NavButton:focus {
            outline: none;
            border: 1px solid #0078D4;
        }

        /* 年月显示标签 - Win11 大标题 */
        #YearMonthLabel {
            font-size: 28px;
            font-weight: 600;
            color: #202020;
            padding: 8px 20px;
            letter-spacing: 0px;
        }

        #YearMonthLabel:hover {
            color: #0078D4;
        }

        /* 底部按钮栏 */
        #BottomButton {
            background-color: #FFFFFF;
            border: 1px solid #E5E5E5;
            border-radius: 6px;
            padding: 10px 18px;
            font-size: 16px;
            color: #1A1A1A;
        }

        #BottomButton:hover {
            background-color: #F5F5F5;
            border-color: #60CDFF;
        }

        /* 日历视图 - Win11 风格 */
        QTableView {
            background-color: transparent;
            border: none;
            gridline-color: transparent;
            selection-background-color: rgba(0, 120, 212, 0.15);
            selection-color: #202020;
            outline: none;
        }

        QTableView::item {
            border: none;
            padding: 2px;
        }

        QTableView::item:selected {
            background-color: rgba(0, 120, 212, 0.12);
        }

        QTableView:focus {
            outline: none;
        }

        /* 水平表头 - Win11 */
        QHeaderView::section {
            background-color: transparent;
            color: #606060;
            font-size: 16px;
            font-weight: 600;
            border: none;
            border-bottom: 1px solid rgba(0, 0, 0, 0.08);
            padding: 12px 8px;
        }

        /* 垂直表头隐藏 */
        QTableView QTableCornerButton::section {
            background-color: transparent;
            border: none;
        }

        /* 对话框 */
        QDialog {
            background-color: #FFFFFF;
        }

        /* 分组框 */
        QGroupBox {
            border: 1px solid #E5E5E5;
            border-radius: 8px;
            margin-top: 16px;
            padding-top: 24px;
            background-color: #FAFAFA;
        }

        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top left;
            left: 16px;
            padding: 0 8px;
            color: #606060;
            font-weight: 600;
        }

        /* 复选框 */
        QCheckBox {
            color: #1A1A1A;
            spacing: 8px;
        }

        QCheckBox::indicator {
            width: 20px;
            height: 20px;
            border: 2px solid #C0C0C0;
            border-radius: 4px;
            background-color: #FFFFFF;
        }

        QCheckBox::indicator:checked {
            background-color: #60CDFF;
            border-color: #60CDFF;
        }

        QCheckBox::indicator:hover {
            border-color: #60CDFF;
        }

        /* 文本编辑 */
        QTextEdit {
            background-color: #FFFFFF;
            border: 1px solid #E5E5E5;
            border-radius: 6px;
            padding: 8px;
            color: #1A1A1A;
            selection-background-color: rgba(96, 205, 255, 0.3);
        }

        QTextEdit:focus {
            border: 2px solid #60CDFF;
        }

        /* 下拉框 */
        QComboBox {
            background-color: #FFFFFF;
            border: 1px solid #E5E5E5;
            border-radius: 6px;
            padding: 8px 12px;
            min-width: 100px;
            color: #1A1A1A;
        }

        QComboBox:hover {
            border-color: #60CDFF;
        }

        QComboBox::drop-down {
            border: none;
            width: 24px;
        }

        QComboBox::down-arrow {
            image: none;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 6px solid #808080;
            margin-right: 8px;
        }

        /* 数字调整框 */
        QSpinBox {
            background-color: #FFFFFF;
            border: 1px solid #E5E5E5;
            border-radius: 6px;
            padding: 8px 12px;
            color: #1A1A1A;
        }

        QSpinBox:hover {
            border-color: #60CDFF;
        }

        QSpinBox::up-button, QSpinBox::down-button {
            background-color: transparent;
            border: none;
            width: 16px;
        }

        /* 按钮盒子 */
        QDialogButtonBox {
            button-layout: 0;
        }

        QDialogButtonBox QPushButton {
            min-width: 80px;
        }

        QDialogButtonBox QPushButton[text="OK"],
        QDialogButtonBox QPushButton[text="确定"] {
            background-color: #60CDFF;
            border-color: #60CDFF;
            color: #FFFFFF;
        }

        QDialogButtonBox QPushButton[text="OK"]:hover,
        QDialogButtonBox QPushButton[text="确定"]:hover {
            background-color: #4DB8E8;
        }

        QDialogButtonBox QPushButton[text="Cancel"],
        QDialogButtonBox QPushButton[text="取消"] {
            background-color: #FFFFFF;
            color: #1A1A1A;
        }

        /* 消息框 */
        QMessageBox {
            background-color: #FFFFFF;
        }

        QMessageBox QLabel {
            color: #1A1A1A;
            font-size: 14px;
        }

        /* 工具提示 */
        QToolTip {
            background-color: #FFFFFF;
            border: 1px solid #E5E5E5;
            border-radius: 6px;
            padding: 6px 10px;
            color: #1A1A1A;
            font-size: 13px;
        }

        /* 滚动条 */
        QScrollBar:vertical {
            background-color: transparent;
            width: 10px;
            margin: 0;
        }

        QScrollBar::handle:vertical {
            background-color: #C0C0C0;
            border-radius: 5px;
            min-height: 30px;
        }

        QScrollBar::handle:vertical:hover {
            background-color: #A0A0A0;
        }

        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            height: 0;
        }

        /* 菜单 */
        QMenu {
            background-color: #FFFFFF;
            border: 1px solid #E5E5E5;
            border-radius: 8px;
            padding: 4px;
        }

        QMenu::item {
            padding: 8px 32px 8px 16px;
            border-radius: 4px;
            color: #1A1A1A;
        }

        QMenu::item:selected {
            background-color: #F5F5F5;
        }

        QMenu::separator {
            height: 1px;
            background-color: #E5E5E5;
            margin: 4px 8px;
        }
        """

    @staticmethod
    def _get_dark_theme() -> str:
        """获取深色主题 QSS"""
        return """
        /* 全局 */
        QWidget {
            font-family: "Segoe UI Variable", "Segoe UI", "Microsoft YaHei UI", sans-serif;
            font-size: 15px;
        }

        /* 主窗口 */
        QMainWindow {
            background-color: #202020;
        }

        /* 标签 */
        QLabel {
            color: #FFFFFF;
            background-color: transparent;
        }

        /* 按钮 */
        QPushButton {
            background-color: #3D3D3D;
            border: 1px solid #505050;
            border-radius: 6px;
            padding: 9px 18px;
            color: #E0E0E0;
            min-height: 32px;
            font-size: 16px;
            transition: all 0.2s ease-out;
        }

        QPushButton:hover {
            background-color: #4D4D4D;
            border-color: #60CDFF;
        }

        QPushButton:pressed {
            background-color: #2D2D2D;
            border-color: #60CDFF;
            transform: scale(0.98);
        }

        QPushButton:focus {
            outline: none;
            border-color: #60CDFF;
            box-shadow: 0 0 0 2px rgba(96, 205, 255, 0.25);
        }

        QPushButton:disabled {
            background-color: #2A2A2A;
            color: #707070;
            border-color: #404040;
        }

        QPushButton:default {
            background-color: #60CDFF;
            border-color: #60CDFF;
            color: #1A1A1A;
            font-weight: 600;
            transition: all 0.2s ease-out;
        }

        QPushButton:default:hover {
            background-color: #4DB8E8;
        }

        QPushButton:default:pressed {
            background-color: #3DA8D8;
            transform: scale(0.98);
        }

        /* 顶部标题区域 */
        #HeaderWidget {
            background-color: #2A2A2E;
            border-bottom: 1px solid #3D3D40;
            border-radius: 12px 12px 0 0;
        }

        /* 导航按钮 */
        #NavButton {
            background-color: #3A3A3E;
            border: 1px solid #4A4A50;
            border-radius: 10px;
            font-size: 20px;
            color: #B0B0B0;
            transition: all 0.2s ease-out;
        }

        #NavButton:hover {
            background-color: #404048;
            border-color: #60CDFF;
            color: #60CDFF;
        }

        #NavButton:pressed {
            background-color: #303038;
            transform: scale(0.95);
        }

        #NavButton:focus {
            outline: none;
            border-color: #60CDFF;
            box-shadow: 0 0 0 2px rgba(96, 205, 255, 0.25);
        }

        /* 年月显示标签 */
        #YearMonthLabel {
            font-size: 28px;
            font-weight: 600;
            color: #E8E8E8;
            padding: 8px 28px;
            letter-spacing: 0px;
        }

        #YearMonthLabel:hover {
            color: #60CDFF;
        }

        /* 底部按钮栏 */
        #BottomButton {
            background-color: #3D3D3D;
            border: 1px solid #505050;
            border-radius: 6px;
            padding: 10px 18px;
            font-size: 16px;
            color: #E0E0E0;
        }

        #BottomButton:hover {
            background-color: #4D4D4D;
            border-color: #60CDFF;
        }

        /* 日历视图 */
        QTableView {
            background-color: #2C2C2C;
            border: none;
            gridline-color: #404040;
            selection-background-color: rgba(96, 205, 255, 0.25);
            selection-color: #E0E0E0;
            outline: none;
        }

        QTableView::item {
            border: none;
            padding: 0;
        }

        QTableView::item:selected {
            background-color: rgba(96, 205, 255, 0.2);
        }

        QTableView:focus {
            outline: none;
        }

        /* 水平表头 */
        QHeaderView::section {
            background-color: #2A2A2E;
            color: #C0C0C0;
            font-size: 16px;
            font-weight: 700;
            border: none;
            padding: 12px;
        }

        /* 垂直表头隐藏 */
        QTableView QTableCornerButton::section {
            background-color: transparent;
            border: none;
        }

        /* 对话框 */
        QDialog {
            background-color: #2C2C2C;
        }

        /* 分组框 */
        QGroupBox {
            border: 1px solid #404040;
            border-radius: 8px;
            margin-top: 16px;
            padding-top: 24px;
            background-color: #252525;
        }

        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top left;
            left: 16px;
            padding: 0 8px;
            color: #A0A0A0;
            font-weight: 600;
        }

        /* 复选框 */
        QCheckBox {
            color: #E0E0E0;
            spacing: 8px;
        }

        QCheckBox::indicator {
            width: 20px;
            height: 20px;
            border: 2px solid #606060;
            border-radius: 4px;
            background-color: #3D3D3D;
        }

        QCheckBox::indicator:checked {
            background-color: #60CDFF;
            border-color: #60CDFF;
        }

        QCheckBox::indicator:hover {
            border-color: #60CDFF;
        }

        /* 文本编辑 */
        QTextEdit {
            background-color: #3D3D3D;
            border: 1px solid #505050;
            border-radius: 6px;
            padding: 8px;
            color: #E0E0E0;
            selection-background-color: rgba(96, 205, 255, 0.4);
        }

        QTextEdit:focus {
            border: 2px solid #60CDFF;
        }

        /* 下拉框 */
        QComboBox {
            background-color: #3D3D3D;
            border: 1px solid #505050;
            border-radius: 6px;
            padding: 8px 12px;
            min-width: 100px;
            color: #E0E0E0;
        }

        QComboBox:hover {
            border-color: #60CDFF;
        }

        QComboBox::drop-down {
            border: none;
            width: 24px;
        }

        QComboBox::down-arrow {
            image: none;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 6px solid #808080;
            margin-right: 8px;
        }

        /* 数字调整框 */
        QSpinBox {
            background-color: #3D3D3D;
            border: 1px solid #505050;
            border-radius: 6px;
            padding: 8px 12px;
            color: #E0E0E0;
        }

        QSpinBox:hover {
            border-color: #60CDFF;
        }

        QSpinBox::up-button, QSpinBox::down-button {
            background-color: transparent;
            border: none;
            width: 16px;
        }

        /* 按钮盒子 */
        QDialogButtonBox {
            button-layout: 0;
        }

        QDialogButtonBox QPushButton {
            min-width: 80px;
        }

        QDialogButtonBox QPushButton[text="OK"],
        QDialogButtonBox QPushButton[text="确定"] {
            background-color: #60CDFF;
            border-color: #60CDFF;
            color: #1A1A1A;
        }

        QDialogButtonBox QPushButton[text="OK"]:hover,
        QDialogButtonBox QPushButton[text="确定"]:hover {
            background-color: #4DB8E8;
        }

        QDialogButtonBox QPushButton[text="Cancel"],
        QDialogButtonBox QPushButton[text="取消"] {
            background-color: #3D3D3D;
            color: #E0E0E0;
        }

        /* 消息框 */
        QMessageBox {
            background-color: #2C2C2C;
        }

        QMessageBox QLabel {
            color: #E0E0E0;
            font-size: 14px;
        }

        /* 工具提示 */
        QToolTip {
            background-color: #3D3D3D;
            border: 1px solid #505050;
            border-radius: 6px;
            padding: 6px 10px;
            color: #E0E0E0;
            font-size: 13px;
        }

        /* 滚动条 */
        QScrollBar:vertical {
            background-color: transparent;
            width: 10px;
            margin: 0;
        }

        QScrollBar::handle:vertical {
            background-color: #606060;
            border-radius: 5px;
            min-height: 30px;
        }

        QScrollBar::handle:vertical:hover {
            background-color: #707070;
        }

        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            height: 0;
        }

        /* 菜单 */
        QMenu {
            background-color: #2C2C2C;
            border: 1px solid #404040;
            border-radius: 8px;
            padding: 4px;
        }

        QMenu::item {
            padding: 8px 32px 8px 16px;
            border-radius: 4px;
            color: #E0E0E0;
        }

        QMenu::item:selected {
            background-color: #3D3D3D;
        }

        QMenu::separator {
            height: 1px;
            background-color: #404040;
            margin: 4px 8px;
        }
        """
