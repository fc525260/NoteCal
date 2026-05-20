"""Window event policies."""

from .data_manager import DataManager
from .tray_controller import TrayController


def should_minimize_to_tray(
    data_manager: DataManager,
    tray_controller: TrayController,
) -> bool:
    """Return whether closing the main window should minimize it to tray."""
    return (
        data_manager.get_setting("minimize_to_tray", True)
        and tray_controller.is_visible()
    )
