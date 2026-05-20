from src.app_metadata import DEFAULT_VERSION, get_project_version


def test_get_project_version_reads_pyproject_version(tmp_path) -> None:
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text(
        '[project]\nname = "notecal"\nversion = "1.2.3"\n',
        encoding="utf-8",
    )

    assert get_project_version(pyproject) == "1.2.3"


def test_get_project_version_returns_default_for_missing_file(tmp_path) -> None:
    assert get_project_version(tmp_path / "missing.toml") == DEFAULT_VERSION


def test_get_project_version_returns_default_without_version(tmp_path) -> None:
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text('[project]\nname = "notecal"\n', encoding="utf-8")

    assert get_project_version(pyproject) == DEFAULT_VERSION
