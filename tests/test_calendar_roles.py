from PyQt5.QtCore import Qt

from src.calendar_model import CalendarModel
from src.calendar_roles import ALL_CALENDAR_ROLES, CalendarRole


def test_calendar_roles_are_unique_and_contiguous() -> None:
    values = [int(role) for role in ALL_CALENDAR_ROLES]

    assert len(values) == len(set(values))
    assert values == list(
        range(Qt.UserRole + 1, Qt.UserRole + 1 + len(ALL_CALENDAR_ROLES))
    )


def test_calendar_model_keeps_legacy_role_aliases() -> None:
    assert CalendarModel.ROLE_DAY == CalendarRole.DAY
    assert CalendarModel.ROLE_YEAR == CalendarRole.YEAR
    assert CalendarModel.ROLE_MONTH == CalendarRole.MONTH
    assert CalendarModel.ROLE_DATE_STRING == CalendarRole.DATE_STRING
    assert CalendarModel.ROLE_IS_TODAY == CalendarRole.IS_TODAY
    assert CalendarModel.ROLE_HAS_NOTE == CalendarRole.HAS_NOTE
    assert CalendarModel.ROLE_LUNAR == CalendarRole.LUNAR
    assert CalendarModel.ROLE_OVERTIME == CalendarRole.OVERTIME
    assert CalendarModel.ROLE_BUSINESS_TRIP == CalendarRole.BUSINESS_TRIP
    assert CalendarModel.ROLE_IS_MARKED == CalendarRole.IS_MARKED
