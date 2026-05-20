"""System tray integration."""

import logging
from typing import Callable, Optional

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QMenu, QSystemTrayIcon, QWidget

logger = logging.getLogger(__name__)


class TrayController:
    """Create and manage the application tray icon."""

    def __init__(
        self,
        parent: QWidget,
        icon_provider: Callable[[], QIcon],
        show_window: Callable[[], None],
        toggle_theme: Callable[[], None],
        quit_application: Callable[[], None],
        toggle_window_visibility: Callable[[], None],
    ) -> None:
        self._parent = parent
        self._icon_provider = icon_provider
        self._show_window = show_window
        self._toggle_theme = toggle_theme
        self._quit_application = quit_application
        self._toggle_window_visibility = toggle_window_visibility
        self.tray_icon: Optional[QSystemTrayIcon] = None

    def initialize(self) -> QSystemTrayIcon | None:
        """Initialize and show the tray icon when the system supports it."""
        if not QSystemTrayIcon.isSystemTrayAvailable():
            logger.warning("系统托盘不可用")
            return None

        tray_icon = QSystemTrayIcon(self._parent)
        tray_icon.setIcon(self._icon_provider())
        tray_icon.setToolTip("日历笔记")
        tray_icon.setContextMenu(self._create_menu())
        tray_icon.activated.connect(self._on_activated)
        tray_icon.show()

        self.tray_icon = tray_icon
        return tray_icon

    def hide(self) -> None:
        """Hide the tray icon if it exists."""
        if self.tray_icon is not None:
            self.tray_icon.hide()

    def is_visible(self) -> bool:
        """Return whether the tray icon currently exists and is visible."""
        return self.tray_icon is not None and self.tray_icon.isVisible()

    def _create_menu(self) -> QMenu:
        tray_menu = QMenu()

        show_action = QAction("显示", self._parent)
        show_action.triggered.connect(self._show_window)
        show_action.setShortcut("Ctrl+Shift+N")
        tray_menu.addAction(show_action)

        theme_action = QAction("切换主题", self._parent)
        theme_action.triggered.connect(self._toggle_theme)
        tray_menu.addAction(theme_action)

        tray_menu.addSeparator()

        quit_action = QAction("退出", self._parent)
        quit_action.triggered.connect(self._quit_application)
        tray_menu.addAction(quit_action)

        return tray_menu

    def _on_activated(self, reason: QSystemTrayIcon.ActivationReason) -> None:
        if reason == QSystemTrayIcon.DoubleClick:
            self._toggle_window_visibility()
