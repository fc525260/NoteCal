"""
主题管理模块

提供 Win11 Fluent 风格的 QSS 样式表，支持浅色/深色模式切换。
"""

import logging
from string import Template
from typing import Optional

logger = logging.getLogger(__name__)


THEME_PALETTES = {
    "light": {
        "window_bg": "#F9F9F9",
        "dialog_bg": "#FFFFFF",
        "panel_bg": "#FAFAFA",
        "control_bg": "#FFFFFF",
        "button_bg": "rgba(249, 249, 249, 0.8)",
        "button_hover_bg": "rgba(249, 249, 249, 0.95)",
        "button_pressed_bg": "#E5E5E5",
        "button_disabled_bg": "transparent",
        "bottom_button_bg": "#FFFFFF",
        "bottom_button_hover_bg": "#F5F5F5",
        "nav_button_bg": "transparent",
        "nav_button_hover_bg": "rgba(0, 0, 0, 0.05)",
        "nav_button_pressed_bg": "rgba(0, 0, 0, 0.1)",
        "table_bg": "transparent",
        "table_grid": "transparent",
        "header_bg": "transparent",
        "header_border": "rgba(0, 0, 0, 0.08)",
        "text": "#202020",
        "muted_text": "#606060",
        "button_text": "#202020",
        "disabled_text": "#A0A0A0",
        "primary_text": "#FFFFFF",
        "field_text": "#1A1A1A",
        "border": "#E5E5E5",
        "subtle_border": "rgba(0, 0, 0, 0.05)",
        "checkbox_border": "#C0C0C0",
        "accent": "#0078D4",
        "accent_hover": "#106EBE",
        "accent_pressed": "#005A9E",
        "field_accent": "#60CDFF",
        "field_accent_hover": "#4DB8E8",
        "selection_bg": "rgba(0, 120, 212, 0.15)",
        "item_selection_bg": "rgba(0, 120, 212, 0.12)",
        "text_selection_bg": "rgba(96, 205, 255, 0.3)",
        "scrollbar": "#C0C0C0",
        "scrollbar_hover": "#A0A0A0",
        "menu_selected_bg": "#F5F5F5",
    },
    "dark": {
        "window_bg": "#202020",
        "dialog_bg": "#2C2C2C",
        "panel_bg": "#252525",
        "control_bg": "#3D3D3D",
        "button_bg": "#3D3D3D",
        "button_hover_bg": "#4D4D4D",
        "button_pressed_bg": "#2D2D2D",
        "button_disabled_bg": "#2A2A2A",
        "bottom_button_bg": "#3D3D3D",
        "bottom_button_hover_bg": "#4D4D4D",
        "nav_button_bg": "#3A3A3E",
        "nav_button_hover_bg": "#404048",
        "nav_button_pressed_bg": "#303038",
        "table_bg": "#2C2C2C",
        "table_grid": "#404040",
        "header_bg": "#2A2A2E",
        "header_border": "#3D3D40",
        "text": "#E8E8E8",
        "muted_text": "#C0C0C0",
        "button_text": "#E0E0E0",
        "disabled_text": "#707070",
        "primary_text": "#1A1A1A",
        "field_text": "#E0E0E0",
        "border": "#505050",
        "subtle_border": "#404040",
        "checkbox_border": "#606060",
        "accent": "#60CDFF",
        "accent_hover": "#4DB8E8",
        "accent_pressed": "#3DA8D8",
        "field_accent": "#60CDFF",
        "field_accent_hover": "#4DB8E8",
        "selection_bg": "rgba(96, 205, 255, 0.25)",
        "item_selection_bg": "rgba(96, 205, 255, 0.2)",
        "text_selection_bg": "rgba(96, 205, 255, 0.4)",
        "scrollbar": "#606060",
        "scrollbar_hover": "#707070",
        "menu_selected_bg": "#3D3D3D",
    },
}


STYLESHEET_TEMPLATE = Template(
    """
    QWidget {
        font-family: "Segoe UI Variable", "Segoe UI", "Microsoft YaHei UI", sans-serif;
        font-size: 15px;
    }

    QMainWindow {
        background-color: $window_bg;
    }

    QLabel {
        color: $text;
        background-color: transparent;
    }

    QPushButton {
        background-color: $button_bg;
        border: 1px solid $subtle_border;
        border-radius: 6px;
        padding: 8px 20px;
        color: $button_text;
        min-height: 32px;
        font-size: 16px;
    }

    QPushButton:hover {
        background-color: $button_hover_bg;
        border-color: $field_accent;
    }

    QPushButton:pressed {
        background-color: $button_pressed_bg;
        border-color: $field_accent;
    }

    QPushButton:focus {
        outline: none;
        border-color: $accent;
    }

    QPushButton:disabled {
        background-color: $button_disabled_bg;
        color: $disabled_text;
        border-color: $subtle_border;
    }

    QPushButton:default {
        background-color: $accent;
        color: $primary_text;
        border-color: $accent;
        font-weight: 600;
    }

    QPushButton:default:hover {
        background-color: $accent_hover;
    }

    QPushButton:default:pressed {
        background-color: $accent_pressed;
    }

    #HeaderWidget {
        background-color: $header_bg;
        border-bottom: 1px solid $header_border;
    }

    #NavButton {
        background-color: $nav_button_bg;
        border: 1px solid $subtle_border;
        border-radius: 6px;
        font-size: 20px;
        color: $muted_text;
        min-width: 38px;
        min-height: 38px;
        padding: 4px 8px;
    }

    #NavButton:hover {
        background-color: $nav_button_hover_bg;
        border-color: $field_accent;
        color: $accent;
    }

    #NavButton:pressed {
        background-color: $nav_button_pressed_bg;
    }

    #NavButton:focus {
        outline: none;
        border-color: $accent;
    }

    #YearMonthLabel {
        font-size: 28px;
        font-weight: 600;
        color: $text;
        padding: 8px 20px;
        letter-spacing: 0px;
    }

    #YearMonthLabel:hover {
        color: $accent;
    }

    #BottomButton {
        background-color: $bottom_button_bg;
        border: 1px solid $border;
        border-radius: 6px;
        padding: 10px 18px;
        font-size: 16px;
        color: $button_text;
    }

    #BottomButton:hover {
        background-color: $bottom_button_hover_bg;
        border-color: $field_accent;
        color: $text;
    }

    #BottomButton:pressed {
        background-color: $button_pressed_bg;
    }

    QTableView {
        background-color: $table_bg;
        border: none;
        gridline-color: $table_grid;
        selection-background-color: $selection_bg;
        selection-color: $text;
        outline: none;
    }

    QTableView::item {
        border: none;
        padding: 2px;
    }

    QTableView::item:selected {
        background-color: $item_selection_bg;
    }

    QTableView:focus {
        outline: none;
    }

    QHeaderView::section {
        background-color: $header_bg;
        color: $muted_text;
        font-size: 16px;
        font-weight: 600;
        border: none;
        border-bottom: 1px solid $header_border;
        padding: 12px 8px;
    }

    QTableView QTableCornerButton::section {
        background-color: transparent;
        border: none;
    }

    QDialog {
        background-color: $dialog_bg;
    }

    QGroupBox {
        border: 1px solid $subtle_border;
        border-radius: 8px;
        margin-top: 16px;
        padding-top: 24px;
        background-color: $panel_bg;
    }

    QGroupBox::title {
        subcontrol-origin: margin;
        subcontrol-position: top left;
        left: 16px;
        padding: 0 8px;
        color: $muted_text;
        font-weight: 600;
    }

    QCheckBox {
        color: $field_text;
        spacing: 8px;
    }

    QCheckBox::indicator {
        width: 20px;
        height: 20px;
        border: 2px solid $checkbox_border;
        border-radius: 4px;
        background-color: $control_bg;
    }

    QCheckBox::indicator:checked {
        background-color: $field_accent;
        border-color: $field_accent;
    }

    QCheckBox::indicator:hover {
        border-color: $field_accent;
    }

    QTextEdit {
        background-color: $control_bg;
        border: 1px solid $border;
        border-radius: 6px;
        padding: 8px;
        color: $field_text;
        selection-background-color: $text_selection_bg;
    }

    QTextEdit:focus {
        border: 2px solid $field_accent;
    }

    QComboBox {
        background-color: $control_bg;
        border: 1px solid $border;
        border-radius: 6px;
        padding: 8px 12px;
        min-width: 100px;
        color: $field_text;
    }

    QComboBox:hover {
        border-color: $field_accent;
    }

    QComboBox::drop-down {
        border: none;
        width: 24px;
    }

    QComboBox::down-arrow {
        image: none;
        border-left: 5px solid transparent;
        border-right: 5px solid transparent;
        border-top: 6px solid $muted_text;
        margin-right: 8px;
    }

    QSpinBox {
        background-color: $control_bg;
        border: 1px solid $border;
        border-radius: 6px;
        padding: 8px 12px;
        color: $field_text;
    }

    QSpinBox:hover {
        border-color: $field_accent;
    }

    QSpinBox::up-button,
    QSpinBox::down-button {
        background-color: transparent;
        border: none;
        width: 16px;
    }

    QDialogButtonBox {
        button-layout: 0;
    }

    QDialogButtonBox QPushButton {
        min-width: 80px;
    }

    QDialogButtonBox QPushButton[text="OK"],
    QDialogButtonBox QPushButton[text="确定"] {
        background-color: $field_accent;
        border-color: $field_accent;
        color: $primary_text;
    }

    QDialogButtonBox QPushButton[text="OK"]:hover,
    QDialogButtonBox QPushButton[text="确定"]:hover {
        background-color: $field_accent_hover;
    }

    QDialogButtonBox QPushButton[text="Cancel"],
    QDialogButtonBox QPushButton[text="取消"] {
        background-color: $control_bg;
        color: $field_text;
    }

    QMessageBox {
        background-color: $dialog_bg;
    }

    QMessageBox QLabel {
        color: $field_text;
        font-size: 14px;
    }

    QToolTip {
        background-color: $control_bg;
        border: 1px solid $border;
        border-radius: 6px;
        padding: 6px 10px;
        color: $field_text;
        font-size: 13px;
    }

    QScrollBar:vertical {
        background-color: transparent;
        width: 10px;
        margin: 0;
    }

    QScrollBar::handle:vertical {
        background-color: $scrollbar;
        border-radius: 5px;
        min-height: 30px;
    }

    QScrollBar::handle:vertical:hover {
        background-color: $scrollbar_hover;
    }

    QScrollBar::add-line:vertical,
    QScrollBar::sub-line:vertical {
        height: 0;
    }

    QMenu {
        background-color: $dialog_bg;
        border: 1px solid $subtle_border;
        border-radius: 8px;
        padding: 4px;
    }

    QMenu::item {
        padding: 8px 32px 8px 16px;
        border-radius: 4px;
        color: $field_text;
    }

    QMenu::item:selected {
        background-color: $menu_selected_bg;
    }

    QMenu::separator {
        height: 1px;
        background-color: $subtle_border;
        margin: 4px 8px;
    }
    """
)


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
        if theme in THEME_PALETTES:
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
        new_theme = (
            self.DARK_THEME
            if self._current_theme == self.LIGHT_THEME
            else self.LIGHT_THEME
        )
        self.set_theme(new_theme)
        return new_theme

    def get_stylesheet(self) -> str:
        """获取当前主题的完整 QSS 样式表

        Returns:
            QSS 样式表字符串
        """
        return self._build_stylesheet(self._current_theme)

    def apply_to_widget(self, widget) -> None:
        """应用主题到指定控件

        Args:
            widget: QWidget 实例
        """
        widget.setStyleSheet(self.get_stylesheet())

    @classmethod
    def _build_stylesheet(cls, theme: str) -> str:
        palette = THEME_PALETTES.get(theme, THEME_PALETTES[cls.LIGHT_THEME])
        return STYLESHEET_TEMPLATE.substitute(palette)

    @classmethod
    def _get_light_theme(cls) -> str:
        """获取浅色主题 QSS"""
        return cls._build_stylesheet(cls.LIGHT_THEME)

    @classmethod
    def _get_dark_theme(cls) -> str:
        """获取深色主题 QSS"""
        return cls._build_stylesheet(cls.DARK_THEME)
