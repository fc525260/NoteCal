from src.calendar_core import CalendarCore


def test_get_month_calendar_returns_fixed_six_week_grid() -> None:
    core = CalendarCore()

    month = core.get_month_calendar(2024, 2)

    assert len(month) == 6
    assert all(len(week) == 7 for week in month)
    assert month[0] == [0, 0, 0, 1, 2, 3, 4]
    assert month[4] == [26, 27, 28, 29, 0, 0, 0]
    assert month[5] == [0, 0, 0, 0, 0, 0, 0]


def test_navigate_month_wraps_across_year_boundaries() -> None:
    core = CalendarCore()

    assert core.navigate_month(2024, 12, 1) == (2025, 1)
    assert core.navigate_month(2024, 1, -1) == (2023, 12)
    assert core.navigate_month(2024, 6, 1) == (2024, 7)


def test_get_date_string_zero_pads_parts() -> None:
    core = CalendarCore()

    assert core.get_date_string(2024, 2, 9) == "2024-02-09"


def test_get_lunar_date_string_returns_none_when_lunar_unavailable() -> None:
    core = CalendarCore()
    core.lunar_utils.lunar_available = False

    assert core.get_lunar_date_string(2024, 2, 10) is None
