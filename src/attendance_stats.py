"""Attendance statistics calculation."""

import calendar as cal_module
from dataclasses import dataclass

from .calendar_core import CalendarCore
from .data_manager import DataManager


@dataclass(frozen=True)
class AttendanceStats:
    """Monthly attendance statistics."""

    attendance_days: int
    overtime_days: int
    overtime_dates: list[str]
    business_trip_days: int


def calculate_month_attendance_stats(
    year: int,
    month: int,
    data_manager: DataManager,
    calendar_core: CalendarCore,
) -> AttendanceStats:
    """Calculate attendance statistics for one calendar month."""
    _, days_in_month = cal_module.monthrange(year, month)
    attendance_days = 0
    overtime_days = 0
    overtime_dates: list[str] = []
    business_trip_days = 0

    for day in range(1, days_in_month + 1):
        date_str = calendar_core.get_date_string(year, month, day)
        content, is_overtime, is_business_trip = data_manager.get_note(date_str)

        if content:
            attendance_days += 1
        if is_overtime:
            overtime_days += 1
            overtime_dates.append(f"{month:02d}-{day:02d}")
        if is_business_trip:
            business_trip_days += 1

    return AttendanceStats(
        attendance_days=attendance_days,
        overtime_days=overtime_days,
        overtime_dates=overtime_dates,
        business_trip_days=business_trip_days,
    )
