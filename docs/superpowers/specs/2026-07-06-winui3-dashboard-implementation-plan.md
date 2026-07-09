# NoteCal WinUI 3 Dashboard Redesign Implementation Plan

Date: 2026-07-06

Related design:
- `docs/superpowers/specs/2026-07-06-winui3-dashboard-redesign.md`

## Current Environment Finding

The current machine has .NET SDK 8.0.422 installed. WinUI CLI templates were installed with:

```powershell
dotnet new install Microsoft.WindowsAppSDK.WinUI.CSharp.Templates
```

`NoteCal.WinUI/` was created from the `winui-navview` template and builds successfully. The project is configured as unpackaged self-contained so the debug executable can launch without relying on a separately registered Windows App Runtime.

This plan assumes the target implementation is C# + XAML + WinUI 3 using Windows App SDK.

## Phase 0: Repository Preparation

Goal: prepare the repository without disturbing the existing PyQt app.

Tasks:
- Keep the existing Python/PyQt5 app in place as the behavioral reference.
- Add a new `NoteCal.WinUI/` project folder for the WinUI 3 app.
- Add a shared `NoteCal.Core/` project for testable calendar, note, and statistics logic.
- Add a lightweight `NoteCal.Core.Tests/` console test runner for core behavior.
- Keep runtime data files, build output, private docs, and visual brainstorm files ignored.
- Decide whether the initial WinUI build is unpackaged, packaged, or both.

Validation:
- `git status --short --ignored` shows local-only folders ignored.
- Existing Python checks still pass before the migration begins.
- `dotnet build NoteCal.sln` succeeds.

## Phase 1: WinUI 3 Scaffold

Goal: create a minimal native WinUI 3 app that builds and launches.

Tasks:
- Create `NoteCal.WinUI/NoteCal.WinUI.csproj`.
- Add Windows App SDK package references.
- Add `App.xaml`, `App.xaml.cs`, `MainWindow.xaml`, and `MainWindow.xaml.cs`.
- Set application title and icon.
- Launch a blank shell with `NavigationView`.

Validation:
- `dotnet build NoteCal.WinUI/NoteCal.WinUI.csproj` succeeds, or the Visual Studio/MSBuild equivalent succeeds.
- The app window opens and shows the initial NavigationView shell.

Current status:
- Done. The app now launches to a first dashboard implementation, not only the blank template shell.

## Phase 2: Core C# Services

Goal: port non-UI behavior into testable C# services.

Tasks:
- Add `Models/NoteEntry.cs`.
- Add `Models/CalendarDay.cs`.
- Add `Models/AttendanceStats.cs`.
- Add `Services/NoteRepository.cs`.
- Add `Services/CalendarService.cs`.
- Add `Services/AttendanceStatsService.cs`.
- Preserve JSON compatibility:
  - Legacy string note records load as content-only notes.
  - Existing object records missing `leave` load with `Leave = false`.
  - Empty notes with all flags false are removed.
  - Empty notes with any flag true are preserved.
- Add JSON corruption backup behavior before fallback.

Validation:
- Add unit tests for note loading, saving, legacy compatibility, and corrupted JSON backup.
- Add unit tests for month grid generation and date formatting.

Current status:
- Done. Core models/services exist and tests cover legacy string notes, missing `leave`, leave-only preservation, empty record removal, month grid shape, leave attendance semantics, corrupted JSON backup, summary filtering, persisted summary date selection, and lunar text generation.

## Phase 3: Leave Status Semantics

Goal: implement approved leave behavior before full UI polish.

Tasks:
- Add `Leave` to the note model.
- Add leave read/write support in repository.
- Add leave day counting in attendance stats.
- Ensure attendance excludes leave days.
- Keep overtime, business trip, and leave independent.

Validation:
- Test that leave-only days are preserved.
- Test that content + leave does not count as attendance.
- Test that content without leave counts as attendance.
- Test that overtime, business trip, and leave totals can all count independently.

Current status:
- Done for the core service layer.

## Phase 4: Dashboard ViewModel

Goal: centralize dashboard state and commands.

Tasks:
- Add `MainViewModel`.
- Track current year/month.
- Track selected date.
- Expose day cells with note/status flags.
- Expose monthly stats.
- Add commands:
  - Previous month
  - Today
  - Next month
  - Select date
  - Save selected date
  - Clear selected date
  - Toggle theme or open settings
- Add unsaved-change state for selected-day editing.

Validation:
- ViewModel tests cover month navigation, selected date updates, save/clear behavior, and stats refresh after edits.

Current status:
- Dashboard ViewModel exists in `NoteCal.WinUI/ViewModels/`.
- ViewModel behavior is not yet covered by automated tests.

## Phase 5: Dashboard XAML

Goal: implement the approved WinUI 3 dashboard.

Tasks:
- Build the main shell with `NavigationView`.
- Build the top command area with WinUI command controls.
- Build the monthly stats band with four metrics:
  - Attendance
  - Overtime
  - Business trip
  - Leave
- Build the month calendar surface with a repeat/grid control.
- Build the right-side selected-day detail panel.
- Implement responsive behavior:
  - Desktop width: calendar left, detail panel right.
  - Narrow width: detail panel collapses below calendar or into a flyout/dialog.

Validation:
- Manual launch confirms the app opens directly to the dashboard.
- Changing month updates calendar and totals.
- Selecting a date updates the detail panel.

Current status:
- First dashboard XAML exists in `Pages/HomePage.xaml`.
- Release UI acceptance passes against the portable root `NoteCal.exe`, including note entry, leave toggle, save, work summary dialog, restart reload, and navigation to stats, summary, and settings.
- Full user manual click acceptance is still pending.

## Phase 6: Visual States And Accessibility

Goal: match the approved UI semantics and make statuses understandable.

Tasks:
- Use WinUI theme resources and system accent color.
- Add status dots:
  - Red: note
  - Green: overtime
  - Orange: business trip
  - Yellow: leave
- Preserve stable dot order:
  1. Note
  2. Overtime
  3. Business trip
  4. Leave
- Add accessible names/tooltips for each status.
- Add visible selected state independent from today.
- Verify light and dark theme contrast.

Validation:
- A date with note + leave shows red and yellow dots.
- Leave dot is distinguishable in light and dark themes.
- Status meaning is also available through text, tooltip, or automation name.

## Phase 7: Settings, Theme, And Secondary Views

Goal: restore user-facing parity with the existing app where it fits the new design.

Tasks:
- Add settings page or settings dialog.
- Persist theme setting.
- Persist lunar display setting.
- Preserve minimize-to-tray equivalent only if technically supported and still desired.
- Add attendance detail view if dashboard stats need drill-down.
- Add selected-date work summary flow.

Validation:
- Settings persist after restart.
- Theme changes apply without breaking status contrast.
- Existing user workflows remain reachable.

Current status:
- SettingsPage is connected to real settings for theme, lunar display, and minimize-to-tray preference.
- StatsPage reads real note JSON and provides month navigation.
- SummaryPage remains available as a secondary page.
- The primary work summary workflow is now available directly on the calendar screen through a `工作总结` dialog opened from HomePage.

## Phase 8: Packaging And Acceptance

Goal: produce a Windows build that can be manually accepted.

Tasks:
- Decide packaging mode:
  - Unpackaged exe for simple local distribution.
  - MSIX for Windows-native install/update behavior.
  - Both if needed.
- Build the release artifact.
- Launch the artifact against a temporary data directory or backed-up data.
- Record size, SHA256, and launch behavior.

Validation:
- Release build succeeds.
- App launches without immediate crash.
- Notes and settings persist across restart.
- Dashboard, leave status, stats, theme, and responsive behavior pass manual acceptance.

Current status:
- Portable release layout exists under `dist\NoteCal-0.7.0-winui3-win-x64-portable\`.
- The root contains the user-facing `NoteCal.exe`; runtime files live under `datas\runtime\`; user JSON files are written under `user\`.
- `scripts\smoke-winui-release.ps1` builds, launches, zips, and hashes the portable release.
- `scripts\accept-winui-ui.ps1` verifies the release exe with Windows UI Automation.
- Latest local release zip: `dist\NoteCal-0.7.0-winui3-win-x64-portable.zip`, size 93,993,317 bytes, SHA256 `CBCBF98681E6F2471476D6A1C7DD82A4A1133876EC367813F5F720FCDFB0AFD9`; final GitHub asset will be rebuilt from the `v0.7.0` tag by GitHub Actions.

## Required Completion Evidence

The WinUI 3 rebuild is not complete until all of the following are true:

- A WinUI 3 project exists in the repository.
- The WinUI 3 project builds successfully.
- The app launches to the approved dashboard.
- Leave exists in model, persistence, calendar visual state, selected-day editor, and statistics.
- Leave does not count as attendance.
- Legacy JSON note data loads without manual migration.
- Automated tests cover the core data and statistics rules.
- A release build or launchable debug build has been run.
- Automated UI acceptance has been recorded.

Current evidence:
- Project exists: `NoteCal.WinUI/`.
- Builds: `dotnet build NoteCal.WinUI\NoteCal.WinUI.csproj -p:Platform=x64`.
- Release smoke: portable root `NoteCal.exe` stayed alive for 8 seconds and produced a zip/hash.
- Core tests: `dotnet run --project NoteCal.Core.Tests\NoteCal.Core.Tests.csproj`.
- UI acceptance: `scripts\accept-winui-ui.ps1` verifies note input, leave toggle, summary dialog, save JSON, restart reload, and main navigation.
- Remaining gap: full user manual UI acceptance has not been recorded.
