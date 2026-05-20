# NoteCal

NoteCal is a powerful note and calendar integration application with Win11 Fluent design style.

## What's New

- **Win11 Fluent Style UI** — Rounded cards, soft colors, modern visual effects
- **Dark/Light Theme Toggle** — One-click theme switching
- **QTableView Calendar Grid** — Model/View architecture for cleaner and more efficient code
- **Custom Cell Delegates** — Today highlighting, note markers, lunar calendar display
- **Keyboard Shortcuts** — Left/Right arrows to navigate months, T for today, S for settings, H for theme toggle
- **Code Quality** — Full type annotations, logging instead of print, simplified core logic

## Features

- Seamless integration of notes and calendar
- Lunar calendar date display
- System tray running
- Dark/Light dual themes
- Keyboard shortcut operations

## Installation

Use the project virtual environment. Do not install dependencies globally.

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Usage

### One-click startup (Windows)

Double-click `启动 NoteCal.bat` to launch directly.

Or run manually with a virtual environment:

```powershell
.\.venv\Scripts\python.exe run.py
```

## Development

Run the standard checks before submitting changes:

```powershell
.\.venv\Scripts\python.exe -m ruff check src tests
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe -m compileall -q run.py src tests
```

Build the Windows executable with PyInstaller:

```powershell
.\.venv\Scripts\python.exe -m PyInstaller --noconfirm --clean NoteCal.spec
```

## Keyboard Shortcuts

| Shortcut | Function |
|----------|----------|
| ← / →   | Previous / Next month |
| T       | Jump to today |
| S       | Open settings |
| H       | Toggle theme |
| Esc     | Exit program |

## Project Data

Runtime data is written under `data/`, including notes, settings, and logs. Treat this directory as local user data and do not commit personal data files.

## Language

- [English](./README.md)
- [简体中文](./README.zh-CN.md)

---

*This repository was created by my Hermes Agent.*
