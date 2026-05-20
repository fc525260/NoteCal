from src.calendar_core import CalendarCore
from src.calendar_delegate import CalendarDelegate
from src.calendar_model import CalendarModel
from src.main_app import CalendarAppDependencies
from src.theme import ThemeManager


def test_calendar_app_dependencies_use_production_defaults() -> None:
    dependencies = CalendarAppDependencies()

    assert dependencies.data_manager is None
    assert dependencies.calendar_core is None
    assert dependencies.theme_manager is None
    assert dependencies.calendar_model_factory is CalendarModel
    assert dependencies.calendar_delegate_factory is CalendarDelegate


def test_calendar_app_dependencies_accept_injected_core_and_theme() -> None:
    calendar_core = CalendarCore()
    theme_manager = ThemeManager()

    dependencies = CalendarAppDependencies(
        calendar_core=calendar_core,
        theme_manager=theme_manager,
    )

    assert dependencies.calendar_core is calendar_core
    assert dependencies.theme_manager is theme_manager
