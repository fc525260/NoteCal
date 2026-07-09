# NoteCal

[English](./README.md) | [简体中文](./README.zh-CN.md)

NoteCal is a Windows calendar note app for daily work logs, attendance status, lunar dates, and selected-date work summaries.

Version `0.7.0` adds a native WinUI 3 rebuild while keeping the original Python/PyQt app in the repository as a behavior reference.

## Highlights

- WinUI 3 dashboard with a calendar-first workflow.
- Daily note editing directly beside the month calendar.
- Status markers for notes, overtime, business trips, and leave.
- Leave uses a yellow dot and does not count as attendance.
- Work summaries can be opened as a dialog from the calendar screen.
- Real lunar date text in the WinUI calendar.
- Portable Windows release layout with a root `NoteCal.exe`, runtime files under `datas\`, and user data under `user\`.
- Existing Python/PyQt version remains available through `run.py`.

## Download

The `v0.7.0` release asset is:

```text
NoteCal-0.7.0-winui3-win-x64-portable.zip
```

Portable layout after extraction:

```text
NoteCal.exe
datas\runtime\...
user\NoteCal_notes.json
user\NoteCal_settings.json
```

Run `NoteCal.exe` from the extracted folder. Runtime dependencies stay under `datas\`; user notes and settings are stored in `user\`.

## Build And Release

### English

Build the local WinUI portable release:

```powershell
.\scripts\build-winui-release.ps1 -Version 0.7.0
```

Run the local release smoke test:

```powershell
.\scripts\smoke-winui-release.ps1
```

Run the local WinUI UI acceptance test:

```powershell
.\scripts\accept-winui-ui.ps1
```

### 中文

构建本地 WinUI portable 发行版：

```powershell
.\scripts\build-winui-release.ps1 -Version 0.7.0
```

运行本地发行版冒烟测试：

```powershell
.\scripts\smoke-winui-release.ps1
```

运行本地 WinUI UI 自动验收：

```powershell
.\scripts\accept-winui-ui.ps1
```

## Development

Install Python dependencies in the project virtual environment:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Run the Python app:

```powershell
.\.venv\Scripts\python.exe run.py
```

Run standard Python checks:

```powershell
.\.venv\Scripts\python.exe -m ruff check src tests
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe -m compileall -q run.py src tests
```

Run C# Core tests:

```powershell
dotnet run --project NoteCal.Core.Tests\NoteCal.Core.Tests.csproj
```

Build the WinUI app for x64:

```powershell
dotnet restore NoteCal.WinUI\NoteCal.WinUI.csproj -p:Platform=x64 -r win-x64
dotnet build NoteCal.WinUI\NoteCal.WinUI.csproj -p:Platform=x64 --no-restore
```

## Repository Layout

```text
NoteCal.Core/        Shared C# calendar, note, settings, summary, and statistics logic
NoteCal.Core.Tests/  Lightweight C# test runner
NoteCal.WinUI/       WinUI 3 desktop app
NoteCal.Launcher/    Root portable launcher published as NoteCal.exe
src/                 Original Python/PyQt app
tests/               Python tests
scripts/             Build, smoke, and UI acceptance scripts
```

## Data

Python/PyQt runtime data is written under `data/`.

WinUI portable runtime data is written next to the root executable:

```text
user\NoteCal_notes.json
user\NoteCal_settings.json
```

Do not commit runtime data, build output, local logs, or private handoff/audit documents.

## License

MIT
