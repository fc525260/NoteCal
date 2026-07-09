# NoteCal

NoteCal 是一个 Windows 日历笔记工具，用于每日工作记录、出勤状态、农历日期和多日期工作总结。

`0.7.0` 版本新增原生 WinUI 3 重构版本，同时保留原 Python/PyQt 应用作为行为参考。

## 主要更新

- WinUI 3 dashboard，保持月历优先的工作流。
- 每日笔记编辑区与月历同屏显示。
- 支持笔记、加班、出差、请假状态点。
- 请假使用黄色圆点，并且不计入出勤天数。
- 工作总结可直接从月历界面弹窗打开，不需要切换到单独页面。
- WinUI 月历显示真实农历文本。
- Windows portable release 采用根目录 `NoteCal.exe`、运行文件 `datas\`、用户数据 `user\` 的结构。
- 原 Python/PyQt 版本仍可通过 `run.py` 运行。

## 下载

GitHub Releases 会由 GitHub Actions 根据版本 tag 自动构建。

`v0.7.0` 的发行版文件为：

```text
NoteCal-0.7.0-winui3-win-x64-portable.zip
```

解压后的 portable 层级：

```text
NoteCal.exe
datas\runtime\...
user\NoteCal_notes.json
user\NoteCal_settings.json
```

从解压目录运行 `NoteCal.exe`。运行依赖保存在 `datas\`，用户笔记和设置保存在 `user\`。

## 构建与发行

本地构建 release：

```powershell
.\scripts\build-winui-release.ps1 -Version 0.7.0
```

本地 release 冒烟测试：

```powershell
.\scripts\smoke-winui-release.ps1
```

本地 WinUI UI 自动验收：

```powershell
.\scripts\accept-winui-ui.ps1
```

推送 `v0.7.0` 这样的版本 tag 后，GitHub release workflow 会运行 Python 检查、Core 测试、构建 WinUI portable 包，并把 zip 发布到 GitHub Releases。本次 release 说明会列出主要更新：WinUI 3 dashboard、请假状态、月历内工作总结弹窗、真实农历文本，以及 `datas\` / `user\` portable 层级。

## 开发

请在项目虚拟环境中安装 Python 依赖：

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

运行 Python 应用：

```powershell
.\.venv\Scripts\python.exe run.py
```

运行 Python 标准检查：

```powershell
.\.venv\Scripts\python.exe -m ruff check src tests
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe -m compileall -q run.py src tests
```

运行 C# Core 测试：

```powershell
dotnet run --project NoteCal.Core.Tests\NoteCal.Core.Tests.csproj
```

构建 x64 WinUI 应用：

```powershell
dotnet restore NoteCal.WinUI\NoteCal.WinUI.csproj -p:Platform=x64 -r win-x64
dotnet build NoteCal.WinUI\NoteCal.WinUI.csproj -p:Platform=x64 --no-restore
```

## 仓库结构

```text
NoteCal.Core/        共享 C# 日历、笔记、设置、总结和统计逻辑
NoteCal.Core.Tests/  轻量 C# 测试运行器
NoteCal.WinUI/       WinUI 3 桌面应用
NoteCal.Launcher/    portable 根目录启动器，发布为 NoteCal.exe
src/                 原 Python/PyQt 应用
tests/               Python 测试
scripts/             构建、冒烟和 UI 验收脚本
```

## 数据

Python/PyQt 运行时数据写入 `data/`。

WinUI portable 运行时数据写入根目录 exe 同级：

```text
user\NoteCal_notes.json
user\NoteCal_settings.json
```

不要提交运行时数据、构建产物、本地日志或私有交接/审计文档。

## 许可证

MIT
