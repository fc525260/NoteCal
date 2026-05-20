"""Calendar model role definitions."""

from enum import IntEnum

from PyQt5.QtCore import Qt


class CalendarRole(IntEnum):
    """Custom roles exposed by CalendarModel."""

    DAY = Qt.UserRole + 1
    YEAR = Qt.UserRole + 2
    MONTH = Qt.UserRole + 3
    DATE_STRING = Qt.UserRole + 4
    IS_TODAY = Qt.UserRole + 5
    HAS_NOTE = Qt.UserRole + 6
    LUNAR = Qt.UserRole + 7
    OVERTIME = Qt.UserRole + 8
    BUSINESS_TRIP = Qt.UserRole + 9
    IS_MARKED = Qt.UserRole + 10


ALL_CALENDAR_ROLES = tuple(CalendarRole)
