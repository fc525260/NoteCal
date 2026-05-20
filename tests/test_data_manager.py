import json

from src.data_manager import DataManager


def make_manager(tmp_path) -> DataManager:
    data_dir = tmp_path / "data"
    return DataManager(
        str(data_dir / "notes.json"),
        str(data_dir / "settings.json"),
    )


def test_set_note_stores_structured_note_data(tmp_path) -> None:
    manager = make_manager(tmp_path)

    manager.set_note("2024-05-01", "劳动节", overtime=True)

    assert manager.get_note("2024-05-01") == ("劳动节", True, False)


def test_set_note_removes_empty_note_without_flags(tmp_path) -> None:
    manager = make_manager(tmp_path)
    manager.set_note("2024-05-01", "旧内容")

    manager.set_note("2024-05-01", "   ")

    assert manager.get_note("2024-05-01") == ("", False, False)
    assert "2024-05-01" not in manager.notes


def test_get_note_supports_legacy_string_note(tmp_path) -> None:
    manager = make_manager(tmp_path)
    manager.notes["2024-05-01"] = "旧格式"

    assert manager.get_note("2024-05-01") == ("旧格式", False, False)


def test_load_settings_merges_existing_file_with_defaults(tmp_path) -> None:
    manager = make_manager(tmp_path)
    settings_path = tmp_path / "data" / "settings.json"
    settings_path.write_text(
        json.dumps({"theme": "dark"}, ensure_ascii=False),
        encoding="utf-8",
    )

    manager.load_settings()

    assert manager.settings == {
        "theme": "dark",
        "minimize_to_tray": True,
        "show_lunar": True,
    }


def test_save_and_load_notes_round_trip(tmp_path) -> None:
    manager = make_manager(tmp_path)
    manager.set_note("2024-05-01", "内容", business_trip=True)
    manager.save_notes()

    reloaded = make_manager(tmp_path)
    reloaded.load_notes()

    assert reloaded.get_note("2024-05-01") == ("内容", False, True)
