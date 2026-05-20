from src.window_events import should_minimize_to_tray


class FakeDataManager:
    def __init__(self, value: bool) -> None:
        self._value = value

    def get_setting(self, key: str, default=None):
        return self._value


class FakeTrayController:
    def __init__(self, visible: bool) -> None:
        self._visible = visible

    def is_visible(self) -> bool:
        return self._visible


def test_should_minimize_to_tray_requires_setting_and_visible_tray() -> None:
    assert should_minimize_to_tray(FakeDataManager(True), FakeTrayController(True))
    assert not should_minimize_to_tray(FakeDataManager(False), FakeTrayController(True))
    assert not should_minimize_to_tray(FakeDataManager(True), FakeTrayController(False))
