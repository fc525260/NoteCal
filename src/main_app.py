"""
主应用程序模块

日历应用的主窗口，使用 QTableView + CalendarModel + CalendarDelegate 实现现代化日历界面。
支持 Win11 Fluent 风格的浅色/深色主题切换。
"""
import logging
import os
import sys
from dataclasses import dataclass
from datetime import datetime
from typing import Callable, Optional

from PyQt5.QtCore import QModelIndex, Qt, QTimer
from PyQt5.QtGui import QIcon, QKeyEvent, QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QDesktopWidget,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSystemTrayIcon,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from .app_metadata import get_project_version
from .attendance_stats import calculate_month_attendance_stats
from .calendar_core import CalendarCore
from .calendar_delegate import CalendarDelegate
from .calendar_model import CalendarModel
from .data_manager import DataManager
from .dialogs import (
    AttendanceStatsDialog,
    DateNoteDialog,
    SelectedSummaryDialog,
    SettingsDialog,
    YearMonthDialog,
)
from .theme import ThemeManager
from .tray_controller import TrayController
from .window_events import should_minimize_to_tray


def _runtime_root() -> str:
    """Return the writable application root for portable data."""
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _resource_root() -> str:
    """Return the root containing bundled read-only resources."""
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return sys._MEIPASS
    return _runtime_root()


def _setup_logging() -> None:
    """配置日志系统"""
    log_dir = os.path.join(_runtime_root(), "data")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "notecal.log")

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(file_handler)

    if sys.stderr is not None:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(
            logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        )
        root_logger.addHandler(console_handler)


_setup_logging()
logger = logging.getLogger(__name__)


@dataclass
class CalendarAppDependencies:
    """CalendarApp dependency configuration.

    Defaults preserve the current production wiring, while tests or future
    storage/theme implementations can provide substitutes.
    """

    data_manager: Optional[DataManager] = None
    calendar_core: Optional[CalendarCore] = None
    theme_manager: Optional[ThemeManager] = None
    calendar_model_factory: Callable[
        [CalendarCore, DataManager, QMainWindow],
        CalendarModel,
    ] = CalendarModel
    calendar_delegate_factory: Callable[
        [QMainWindow],
        CalendarDelegate,
    ] = CalendarDelegate


class CalendarApp(QMainWindow):
    """日历应用主窗口类

    管理应用的主界面、用户交互和核心业务逻辑，包括日历显示、笔记管理和系统托盘功能。
    使用 QTableView + CalendarModel 实现现代化日历界面。
    """

    def __init__(
        self,
        dependencies: Optional[CalendarAppDependencies] = None,
    ) -> None:
        """初始化日历应用"""
        super().__init__()

        logger.info("正在初始化日历应用...")

        self.dependencies = dependencies or CalendarAppDependencies()

        self.base_dir = self._get_base_dir()
        self.resource_dir = self._get_resource_dir()
        self.user_data_dir = self._get_user_data_dir()

        self._set_directories()

        os.makedirs(self.data_dir, exist_ok=True)

        self.data_manager = self.dependencies.data_manager or self._create_data_manager()
        self.calendar_core = self.dependencies.calendar_core or CalendarCore()
        self.theme_manager = (
            self.dependencies.theme_manager or ThemeManager.get_instance()
        )
        self.selection_mode = False
        self.selected_dates: set[str] = set()

        self.data_manager.load_notes()
        self.data_manager.load_settings()

        theme_setting = self.data_manager.get_setting("theme", "light")
        self.theme_manager.set_theme(theme_setting)

        today = datetime.now()
        self.current_year = today.year
        self.current_month = today.month

        self._init_ui()
        self.tray_controller = self._create_tray_controller()
        self.tray_icon = self.tray_controller.initialize()

        self.calendar_model.set_date(self.current_year, self.current_month)
        self._update_calendar()

        self.timer = QTimer()
        self.timer.timeout.connect(self._update_today_highlight)
        self.timer.start(60000)

        logger.info("日历应用初始化完成")

    def _create_data_manager(self) -> DataManager:
        """Create the default JSON-backed data manager."""
        notes_path = os.path.join(self.data_dir, "NoteCal_notes.json")
        settings_path = os.path.join(self.data_dir, "NoteCal_settings.json")
        return DataManager(notes_path, settings_path)

    def _get_base_dir(self) -> str:
        """获取基础目录"""
        base_dir = _runtime_root()
        if getattr(sys, "frozen", False):
            logger.debug(f"打包环境 - exe目录: {base_dir}")
        else:
            logger.debug(f"开发环境 - 项目根目录: {base_dir}")
        return base_dir

    def _get_resource_dir(self) -> str:
        """获取资源目录根路径"""
        resource_dir = _resource_root()
        logger.debug(f"资源根目录: {resource_dir}")
        return resource_dir

    def _get_user_data_dir(self) -> str:
        """获取用户数据目录"""
        return self.base_dir

    def _set_directories(self) -> None:
        """设置数据目录和资源目录"""
        self.data_dir = os.path.join(self.user_data_dir, "data")
        bundled_assets = os.path.join(self.resource_dir, "assets")
        external_assets = os.path.join(self.base_dir, "assets")
        self.assets_dir = bundled_assets if os.path.exists(bundled_assets) else external_assets

        logger.debug(f"资产目录: {self.assets_dir}")
        logger.debug(f"数据目录: {self.data_dir}")

    def _get_icon(self) -> QIcon:
        """获取程序图标"""
        icon_path = os.path.join(self.assets_dir, "icons", "NoteCal.ico")

        if os.path.exists(icon_path):
            logger.debug(f"加载图标: {icon_path}")
            return QIcon(icon_path)

        logger.debug("使用默认图标")
        pixmap = QPixmap(32, 32)
        pixmap.fill(Qt.blue)
        return QIcon(pixmap)

    def _set_adaptive_geometry(self) -> None:
        """根据屏幕大小自适应设置窗口尺寸"""
        screen = QDesktopWidget().screenGeometry()
        screen_width = screen.width()
        screen_height = screen.height()

        logger.debug(f"屏幕分辨率: {screen_width}x{screen_height}")

        base_size = min(screen_width, screen_height)
        window_width = int(base_size * 0.5)
        window_height = int(window_width * 1.1)

        window_width = max(760, min(1200, window_width))
        window_height = max(520, min(1000, window_height))

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.setGeometry(x, y, window_width, window_height)
        logger.info(f"窗口尺寸: {window_width}x{window_height} (屏幕 {screen_width}x{screen_height})")

    def _init_ui(self) -> None:
        """初始化用户界面"""
        self.setWindowTitle("日历笔记")
        self._set_adaptive_geometry()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(8)
        central_widget.setLayout(main_layout)

        self._create_control_bar(main_layout)
        self._create_calendar_view(main_layout)
        self._create_bottom_bar(main_layout)

        self.setWindowIcon(self._get_icon())

        self.theme_manager.apply_to_widget(self)

    def _create_control_bar(self, parent_layout: QVBoxLayout) -> None:
        """创建顶部控制栏 - 更醒目的设计"""
        header_widget = QWidget()
        header_widget.setObjectName("HeaderWidget")
        header_widget.setMinimumHeight(88)
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(24, 20, 24, 20)
        header_layout.setSpacing(20)

        prev_button = QPushButton("◀")
        prev_button.setObjectName("NavButton")
        prev_button.clicked.connect(self._prev_month)
        prev_button.setToolTip("上一月 (左方向键)")
        prev_button.setFixedSize(48, 48)
        prev_button.setFocusPolicy(Qt.StrongFocus)
        header_layout.addWidget(prev_button)

        header_layout.addStretch()

        self.year_month_label = QLabel()
        self.year_month_label.setObjectName("YearMonthLabel")
        self.year_month_label.setAlignment(Qt.AlignCenter)
        self.year_month_label.mousePressEvent = self._show_year_month_dialog
        self.year_month_label.setCursor(Qt.PointingHandCursor)
        self.year_month_label.setToolTip("点击选择年月")
        header_layout.addWidget(self.year_month_label)

        header_layout.addStretch()

        next_button = QPushButton("▶")
        next_button.setObjectName("NavButton")
        next_button.clicked.connect(self._next_month)
        next_button.setToolTip("下一月 (右方向键)")
        next_button.setFixedSize(48, 48)
        next_button.setFocusPolicy(Qt.StrongFocus)
        header_layout.addWidget(next_button)

        parent_layout.addWidget(header_widget)

    def _create_calendar_view(self, parent_layout: QVBoxLayout) -> None:
        """创建日历视图 (QTableView)"""
        self.calendar_view = QTableView()

        self.calendar_model = self.dependencies.calendar_model_factory(
            self.calendar_core,
            self.data_manager,
            self
        )
        self.calendar_view.setModel(self.calendar_model)

        self.calendar_delegate = self.dependencies.calendar_delegate_factory(self)
        self.calendar_view.setItemDelegate(self.calendar_delegate)

        self.calendar_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.calendar_view.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.calendar_view.horizontalHeader().setFixedHeight(50)

        self.calendar_view.horizontalHeader().setVisible(True)
        self.calendar_view.verticalHeader().setVisible(False)

        self.calendar_view.setShowGrid(False)

        self.calendar_view.setSelectionMode(QTableView.SingleSelection)
        self.calendar_view.setSelectionBehavior(QTableView.SelectItems)

        self.calendar_view.clicked.connect(self._on_cell_clicked)

        self.calendar_view.setFocusPolicy(Qt.ClickFocus)

        parent_layout.addWidget(self.calendar_view, 1)

    def _create_bottom_bar(self, parent_layout: QVBoxLayout) -> None:
        """创建底部按钮栏"""
        bottom_layout = QHBoxLayout()
        bottom_layout.setContentsMargins(0, 10, 0, 0)
        bottom_layout.setSpacing(8)

        today_button = QPushButton("今天")
        today_button.setObjectName("BottomButton")
        today_button.clicked.connect(self._goto_today)
        today_button.setToolTip("跳转到今天 (T 键)")
        bottom_layout.addWidget(today_button)

        stats_button = QPushButton("当月出勤统计")
        stats_button.setObjectName("BottomButton")
        stats_button.clicked.connect(self._show_attendance_stats)
        stats_button.setToolTip("查看当前月份的出勤、加班和出差统计")
        bottom_layout.addWidget(stats_button)

        bottom_layout.addStretch()

        theme_button = QPushButton("主题")
        theme_button.setObjectName("BottomButton")
        theme_button.clicked.connect(self._toggle_theme)
        theme_button.setToolTip("切换浅色/深色模式")
        bottom_layout.addWidget(theme_button)

        settings_button = QPushButton("设置")
        settings_button.setObjectName("BottomButton")
        settings_button.clicked.connect(self._show_settings)
        settings_button.setToolTip("打开设置 (S 键)")
        bottom_layout.addWidget(settings_button)

        self.select_dates_button = QPushButton("选择日期")
        self.select_dates_button.setObjectName("BottomButton")
        self.select_dates_button.clicked.connect(self._handle_select_dates_button)
        self.select_dates_button.setToolTip("选择多个日期并生成工作总结")
        bottom_layout.addWidget(self.select_dates_button)

        self.cancel_selection_button = QPushButton("取消选择")
        self.cancel_selection_button.setObjectName("BottomButton")
        self.cancel_selection_button.clicked.connect(self._exit_selection_mode)
        self.cancel_selection_button.setToolTip("退出日期选择模式")
        self.cancel_selection_button.hide()
        bottom_layout.addWidget(self.cancel_selection_button)

        exit_button = QPushButton("退出")
        exit_button.setObjectName("BottomButton")
        exit_button.clicked.connect(self.close)
        exit_button.setToolTip("退出程序 (Esc 键)")
        bottom_layout.addWidget(exit_button)

        parent_layout.addLayout(bottom_layout)

    def _init_tray(self) -> None:
        """初始化系统托盘"""
        self.tray_controller.initialize()

    def _create_tray_controller(self) -> TrayController:
        """Create the system tray controller."""
        return TrayController(
            parent=self,
            icon_provider=self._get_icon,
            show_window=self.show,
            toggle_theme=self._toggle_theme,
            quit_application=self._quit_application,
            toggle_window_visibility=self._toggle_window_visibility,
        )

    def _update_calendar(self) -> None:
        """更新日历显示"""
        self.year_month_label.setText(f"{self.current_year}年 {self.current_month}月")
        self.calendar_model.set_date(self.current_year, self.current_month)

    def _update_today_highlight(self) -> None:
        """更新今天的高亮显示"""
        self.calendar_model.refresh()

    def _on_cell_clicked(self, index: QModelIndex) -> None:
        """处理单元格点击事件"""
        if not index.isValid():
            return

        date_info = self.calendar_model.get_date_info(index.row(), index.column())
        if not date_info:
            return

        date_str = date_info["date_string"]
        if self.selection_mode:
            if date_str in self.selected_dates:
                self.selected_dates.remove(date_str)
            else:
                self.selected_dates.add(date_str)
            self.calendar_model.set_marked_dates(self.selected_dates)
            return

        note_content, is_overtime, is_business_trip = self.data_manager.get_note(date_str)

        dialog = DateNoteDialog(
            date_str,
            note_content,
            is_overtime,
            is_business_trip,
            self
        )
        self.theme_manager.apply_to_widget(dialog)

        if dialog.exec_() == DateNoteDialog.Accepted:
            new_content = dialog.get_note_content()
            new_overtime = dialog.is_overtime()
            new_business_trip = dialog.is_business_trip()
            self.data_manager.set_note(
                date_str,
                new_content,
                new_overtime,
                new_business_trip
            )
            self.data_manager.save_notes()
            self.calendar_model.refresh()

    def _show_attendance_stats(self) -> None:
        """显示当前月份的出勤统计"""
        stats = calculate_month_attendance_stats(
            self.current_year,
            self.current_month,
            self.data_manager,
            self.calendar_core,
        )

        dialog = AttendanceStatsDialog(
            self.current_year,
            self.current_month,
            stats.attendance_days,
            stats.overtime_days,
            stats.overtime_dates,
            stats.business_trip_days,
            self
        )
        self.theme_manager.apply_to_widget(dialog)
        dialog.exec_()

    def _handle_select_dates_button(self) -> None:
        """进入选择模式或生成所选日期总结"""
        if not self.selection_mode:
            self._enter_selection_mode()
            return

        if not self.selected_dates:
            QMessageBox.information(self, "选择日期", "请先选择至少一个日期。")
            return

        summary_text = self._build_selected_summary_text()
        dialog = SelectedSummaryDialog(summary_text, self)
        self.theme_manager.apply_to_widget(dialog)
        dialog.exec_()

    def _enter_selection_mode(self) -> None:
        """进入日期选择模式"""
        self.selection_mode = True
        self.selected_dates.clear()
        self.calendar_model.set_marked_dates(self.selected_dates)
        self.select_dates_button.setText("生成总结")
        self.select_dates_button.setToolTip("生成所选日期的工作总结文本")
        self.cancel_selection_button.show()

    def _exit_selection_mode(self) -> None:
        """退出日期选择模式"""
        self.selection_mode = False
        self.selected_dates.clear()
        self.calendar_model.set_marked_dates(self.selected_dates)
        self.select_dates_button.setText("选择日期")
        self.select_dates_button.setToolTip("选择多个日期并生成工作总结")
        self.cancel_selection_button.hide()

    def _build_selected_summary_text(self) -> str:
        """构建所选日期的工作总结文本"""
        lines = []
        sorted_dates = sorted(self.selected_dates)
        for index, date_str in enumerate(sorted_dates):
            content, _, _ = self.data_manager.get_note(date_str)
            ending = "。" if index == len(sorted_dates) - 1 else ";"
            lines.append(f"{date_str[5:]}工作总结：{content.strip()}{ending}")
        return "\n".join(lines)

    def _prev_month(self) -> None:
        """切换到上一个月"""
        if self.selection_mode:
            self._exit_selection_mode()
        self.current_year, self.current_month = self.calendar_core.navigate_month(
            self.current_year, self.current_month, -1
        )
        self._update_calendar()

    def _next_month(self) -> None:
        """切换到下一个月"""
        if self.selection_mode:
            self._exit_selection_mode()
        self.current_year, self.current_month = self.calendar_core.navigate_month(
            self.current_year, self.current_month, 1
        )
        self._update_calendar()

    def _goto_today(self) -> None:
        """跳转到今天"""
        if self.selection_mode:
            self._exit_selection_mode()
        today = datetime.now()
        self.current_year = today.year
        self.current_month = today.month
        self._update_calendar()

    def _show_year_month_dialog(self, event) -> None:
        """显示年月选择对话框"""
        if self.selection_mode:
            self._exit_selection_mode()
        dialog = YearMonthDialog(self.current_year, self.current_month, self)
        self.theme_manager.apply_to_widget(dialog)

        if dialog.exec_() == YearMonthDialog.Accepted:
            year, month = dialog.get_year_month()
            self.current_year = year
            self.current_month = month
            self._update_calendar()

    def _show_settings(self) -> None:
        """显示设置对话框"""
        dialog = SettingsDialog(self.data_manager.settings, self)
        self.theme_manager.apply_to_widget(dialog)

        if dialog.exec_() == SettingsDialog.Accepted:
            new_settings = dialog.get_settings()
            self.data_manager.settings.update(new_settings)
            self.data_manager.save_settings()

            if "theme" in new_settings:
                self.theme_manager.set_theme(new_settings["theme"])
                self.theme_manager.apply_to_widget(self)

            self._update_calendar()

    def _toggle_theme(self) -> None:
        """切换主题"""
        new_theme = self.theme_manager.toggle_theme()
        self.data_manager.settings["theme"] = new_theme
        self.data_manager.save_settings()

        self.theme_manager.apply_to_widget(self)
        self.calendar_model.refresh()

    def _tray_icon_activated(self, reason: QSystemTrayIcon.ActivationReason) -> None:
        """处理托盘图标激活事件"""
        if reason == QSystemTrayIcon.DoubleClick:
            self._toggle_window_visibility()

    def _toggle_window_visibility(self) -> None:
        """Toggle the main window visibility from tray actions."""
        if self.isVisible():
            self.hide()
        else:
            self.show()
            self.activateWindow()

    def keyPressEvent(self, event: QKeyEvent) -> None:
        """处理键盘事件"""
        key = event.key()

        if key == Qt.Key_Left:
            self._prev_month()
        elif key == Qt.Key_Right:
            self._next_month()
        elif key == Qt.Key_T:
            self._goto_today()
        elif key == Qt.Key_S:
            self._show_settings()
        elif key == Qt.Key_H:
            self._toggle_theme()
        elif key == Qt.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)

    def closeEvent(self, event) -> None:
        """处理窗口关闭事件"""
        if should_minimize_to_tray(self.data_manager, self.tray_controller):
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("系统托盘")
            msg_box.setText("程序将继续在系统托盘中运行。\n要退出程序，请从托盘菜单中选择'退出'。")
            msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            yes_btn = msg_box.button(QMessageBox.Yes)
            no_btn = msg_box.button(QMessageBox.No)
            yes_btn.setText("确认")
            no_btn.setText("取消")
            msg_box.setDefaultButton(QMessageBox.Yes)
            msg_box.setIcon(QMessageBox.Information)

            reply = msg_box.exec_()
            if reply == QMessageBox.Yes:
                self.hide()
                event.ignore()
                return

        self._quit_application()

    def _quit_application(self) -> None:
        """退出应用程序"""
        self.data_manager.save_notes()
        self.data_manager.save_settings()

        self.tray_controller.hide()

        QApplication.quit()


def main() -> None:
    """主函数，程序入口点"""
    try:
        app = QApplication(sys.argv)

        app.setQuitOnLastWindowClosed(False)
        app.setApplicationName("日历笔记")
        app.setApplicationDisplayName("日历笔记")
        app.setOrganizationName("NoteCal")
        app.setApplicationVersion(get_project_version())

        calendar_app = CalendarApp()
        calendar_app.show()

        sys.exit(app.exec_())

    except Exception as e:
        logger.error(f"程序启动失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
