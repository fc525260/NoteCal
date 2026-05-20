from src.lunar_utils import LunarUtils


def test_get_lunar_date_returns_none_when_unavailable() -> None:
    lunar = LunarUtils()
    lunar.lunar_available = False

    assert lunar.get_lunar_date(2024, 2, 10) is None


def test_get_lunar_date_formats_regular_lunar_date() -> None:
    class FakeSolar:
        def __init__(self, year: int, month: int, day: int) -> None:
            self.year = year
            self.month = month
            self.day = day

    class FakeLunarDate:
        month = 1
        day = 1
        isleap = False

    class FakeConverter:
        def Solar2Lunar(self, solar: FakeSolar) -> FakeLunarDate:
            return FakeLunarDate()

    lunar = LunarUtils()
    lunar.lunar_available = True
    lunar.Solar = FakeSolar
    lunar.converter = FakeConverter()

    assert lunar.get_lunar_date(2024, 2, 10) == "正月初一"


def test_get_lunar_date_formats_leap_month() -> None:
    class FakeSolar:
        def __init__(self, year: int, month: int, day: int) -> None:
            self.year = year
            self.month = month
            self.day = day

    class FakeLunarDate:
        month = 2
        day = 3
        isleap = True

    class FakeConverter:
        def Solar2Lunar(self, solar: FakeSolar) -> FakeLunarDate:
            return FakeLunarDate()

    lunar = LunarUtils()
    lunar.lunar_available = True
    lunar.Solar = FakeSolar
    lunar.converter = FakeConverter()

    assert lunar.get_lunar_date(2024, 3, 12) == "闰二月初三"
