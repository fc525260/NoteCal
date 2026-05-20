# NoteCal

NoteCal 是一款功能强大的笔记日历集成应用，采用 Win11 Fluent 风格设计。

## 新功能

- **Win11 Fluent 风格 UI** — 圆角卡片、柔和配色、现代视觉效果
- **深色/浅色主题切换** — 支持主题一键切换
- **QTableView 日历网格** — 使用 Model/View 架构，更规范高效
- **自定义单元格委托** — 绘制今天高亮、笔记标记、农历显示
- **键盘快捷键** — 左/右方向键翻月，T 键今天，S 键设置，H 键主题切换
- **代码质量提升** — 完整类型注解、logging 替代 print、简化核心逻辑

## 功能特点

- 笔记与日历无缝集成
- 农历日期显示支持
- 系统托盘运行
- 深色/浅色双主题
- 键盘快捷操作

## 安装方法

请使用项目自带的虚拟环境安装依赖，不要安装到全局 Python 环境。

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## 使用方法

### 一键启动 (Windows)

双击 `启动 NoteCal.bat` 即可直接运行。

或手动使用虚拟环境运行：

```powershell
.\.venv\Scripts\python.exe run.py
```

## 开发

提交改动前运行标准检查：

```powershell
.\.venv\Scripts\python.exe -m ruff check src tests
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe -m compileall -q run.py src tests
```

使用 PyInstaller 构建 Windows 可执行文件：

```powershell
.\.venv\Scripts\python.exe -m PyInstaller --noconfirm --clean NoteCal.spec
```

## 快捷键

| 快捷键 | 功能 |
|--------|------|
| ← / → | 上一月 / 下一月 |
| T | 跳转到今天 |
| S | 打开设置 |
| H | 切换主题 |
| Esc | 退出程序 |

## 项目数据

运行时数据会写入 `data/`，包括笔记、设置和日志。该目录属于本地用户数据，不应提交个人数据文件。

## 语言

- [English](./README.md)
- [简体中文](./README.zh-CN.md)

---

*此仓库由我的 Hermes Agent 创建。*
