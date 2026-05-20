from src.attendance_stats import AttendanceStats, calculate_month_attendance_stats
from src.calendar_core import CalendarCore
from src.data_manager import DataManager


def make_manager(tmp_path) -> DataManager:
    data_dir = tmp_path / "data"
    return DataManager(
        str(data_dir / "notes.json"),
        str(data_dir / "settings.json"),
    )


def test_calculate_month_attendance_stats_counts_current_month(tmp_path) -> None:
    manager = make_manager(tmp_path)
    core = CalendarCore()
    manager.set_note("2024-05-01", "工作内容")
    manager.set_note("2024-05-02", "", overtime=True)
    manager.set_note("2024-05-03", "出差", business_trip=True)
    manager.set_note("2024-06-01", "其他月份", overtime=True)

    stats = calculate_month_attendance_stats(2024, 5, manager, core)

    assert stats == AttendanceStats(
        attendance_days=2,
        overtime_days=1,
        overtime_dates=["05-02"],
        business_trip_days=1,
    )


def test_calculate_month_attendance_stats_supports_leap_year(tmp_path) -> None:
    manager = make_manager(tmp_path)
    core = CalendarCore()
    manager.set_note("2024-02-29", "闰日", overtime=True, business_trip=True)

    stats = calculate_month_attendance_stats(2024, 2, manager, core)

    assert stats.attendance_days == 1
    assert stats.overtime_days == 1
    assert stats.overtime_dates == ["02-29"]
    assert stats.business_trip_days == 1
