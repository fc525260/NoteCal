# NoteCal WinUI 3 Dashboard Redesign Design

Date: 2026-07-06

## Decision

NoteCal will move toward a native WinUI 3 dashboard interface using Windows App SDK. The approved product direction is the Productivity dashboard layout: calendar remains the main working surface, while monthly status totals and selected-day note editing are always visible.

This is a UI and platform migration direction, not a PyQt skinning pass. The current Python/PyQt5 implementation remains the reference for behavior and business logic, but the target UI layer is C# + XAML on WinUI 3.

Primary references:
- WinUI 3 overview: https://learn.microsoft.com/windows/apps/winui/winui3/
- Windows App SDK: https://learn.microsoft.com/windows/apps/windows-app-sdk/
- WinUI Gallery: https://github.com/microsoft/WinUI-Gallery
- NavigationView: https://learn.microsoft.com/windows/apps/develop/ui/controls/navigationview
- CalendarView: https://learn.microsoft.com/windows/windows-app-sdk/api/winrt/microsoft.ui.xaml.controls.calendarview
- CommandBar: https://learn.microsoft.com/windows/apps/design/controls/command-bar
- ContentDialog: https://learn.microsoft.com/windows/apps/design/controls/dialogs-and-flyouts/dialogs
- InfoBar: https://learn.microsoft.com/windows/apps/design/controls/infobar

## Goals

- Rebuild NoteCal as a modern Windows desktop app using WinUI 3 visual language and native controls.
- Keep the calendar-first workflow: opening the app should immediately show the month calendar.
- Make work status information visible without modal navigation.
- Add a new "leave" status alongside overtime and business trip.
- Preserve existing note data as much as possible through backward-compatible JSON parsing.
- Keep UI behavior efficient for repeated daily work logging.

## Non-Goals

- Do not keep PyQt as the long-term UI framework for this redesign.
- Do not add cloud sync, accounts, reminders, recurrence, or calendar service integration in this change.
- Do not change the meaning of existing overtime or business trip data.
- Do not require existing users to manually migrate JSON data.
- Do not publish local handoff/audit documents.

## Product Layout

The app shell uses a left `NavigationView` with these top-level areas:

- Month calendar
- Work summary
- Attendance statistics
- Settings

The primary work summary action is also available directly from the Month calendar screen as a dialog, so users can select dates and generate the summary without leaving the calendar workflow.

The default selected route is Month calendar. The main content is a dashboard with three vertical regions:

1. Command area
   - Current year/month title
   - Previous month
   - Today
   - Next month
   - Select dates
   - Settings/theme access

2. Monthly status totals
   - Attendance days
   - Overtime days
   - Business trip days
   - Leave days

3. Work surface
   - Left: month calendar grid
   - Right: selected-day detail panel with note editor and status checkboxes

On narrow windows, the selected-day panel may collapse below the calendar or become a flyout/dialog. The calendar must remain the primary visible element.

## Calendar Visual States

Date cells expose these independent visual states:

- Today: WinUI accent-colored background.
- Selected: visible selection border or selection state, separate from today.
- Has note: red status dot.
- Overtime: green status dot.
- Business trip: orange status dot.
- Leave: yellow status dot.

When multiple statuses apply to the same date, dots appear in a stable order:

1. Note
2. Overtime
3. Business trip
4. Leave

The leave dot is yellow and should include sufficient contrast in both light and dark themes. If the yellow fill is too low contrast on light surfaces, use a thin neutral outline.

## Selected-Day Detail Panel

The right panel shows the selected date and edits the selected date in place.

Controls:
- Date heading
- Lunar date text if lunar display is enabled
- Multiline note editor
- Overtime checkbox
- Business trip checkbox
- Leave checkbox
- Work summary dialog action for selected dates
- Save action
- Clear action

Behavior:
- Selecting a date updates the panel without opening a modal.
- Generating a work summary may open a modal dialog, but it starts from the calendar screen.
- Save writes the current note and status flags.
- Clear removes note content and clears all status flags for that date.
- If the user selects another date with unsaved changes, the app should either save automatically or prompt clearly. The preferred first implementation is explicit save with a clear unsaved indicator.

## Data Model

Existing note records currently support:

```json
{
  "content": "",
  "overtime": false,
  "business_trip": false
}
```

The new record shape adds `leave`:

```json
{
  "content": "",
  "overtime": false,
  "business_trip": false,
  "leave": false
}
```

Backward compatibility:
- Existing string note records are read as content-only records.
- Existing object records missing `leave` are read with `leave = false`.
- Empty content with all flags false means the date record can be removed.
- Empty content with any status flag true must be preserved.

## Attendance Semantics

The approved rule is:

- Leave days do not count as attendance days.

Monthly statistics:

- `attendance_days`: count dates where content is non-empty and `leave == false`.
- `overtime_days`: count dates where `overtime == true`.
- `business_trip_days`: count dates where `business_trip == true`.
- `leave_days`: count dates where `leave == true`.
- Optional lists for display/export:
  - `overtime_dates`
  - `business_trip_dates`
  - `leave_dates`

If a date has both note content and leave, it shows both the note dot and leave dot, but it does not count toward attendance days.

## Architecture

Target project shape:

- `NoteCal.WinUI/`
  - C# WinUI 3 application project.
  - XAML views and view models.
  - Windows App SDK package references.

Recommended C# components:

- `Models/NoteEntry.cs`
  - `Content`
  - `Overtime`
  - `BusinessTrip`
  - `Leave`

- `Services/NoteRepository.cs`
  - Loads/saves JSON.
  - Handles legacy string and missing-field compatibility.

- `Services/CalendarService.cs`
  - Month grid generation.
  - Date formatting.
  - Today detection.

- `Services/AttendanceStatsService.cs`
  - Monthly statistics with approved leave semantics.

- `ViewModels/MainViewModel.cs`
  - Current year/month.
  - Selected date.
  - Calendar day view models.
  - Command handlers.

- `Views/MainWindow.xaml`
  - NavigationView shell.
  - Dashboard layout.
  - CommandBar.
  - Calendar grid.
  - Detail panel.

The existing Python modules are behavioral references during migration:

- `src/data_manager.py`
- `src/calendar_core.py`
- `src/attendance_stats.py`
- `src/calendar_model.py`
- `src/main_app.py`

## Error Handling

- JSON load failure should not silently destroy user data.
- If JSON parsing fails, keep the bad file and write a timestamped backup before creating a fresh in-memory state.
- Save failures should show an `InfoBar` with a clear message.
- Missing lunar conversion support should degrade by hiding lunar text, not by blocking the calendar.
- Invalid settings values should fall back to defaults.

## Theme And Accessibility

- Use WinUI theme resources and system accent color where practical.
- Support light and dark themes.
- Preserve keyboard access for month navigation, today, settings, and save.
- All icon-only commands need accessible names.
- Status meaning must not rely on color alone; use tooltip, automation name, or detail text labels.
- Keep hit targets at least 44x44 effective pixels for primary controls.

## Migration Plan Boundary

This design expects implementation to proceed in phases:

1. Verify local WinUI 3 build environment.
2. Scaffold a C# WinUI 3 app.
3. Port JSON data model and services.
4. Implement dashboard UI.
5. Implement leave status across model, UI, and statistics.
6. Add focused tests for JSON compatibility and statistics semantics.
7. Build and launch the Windows app for manual acceptance.

## Validation Criteria

Automated validation:

- Legacy string notes load correctly.
- Object notes missing `leave` load with `leave = false`.
- Leave-only records are preserved.
- Empty records with no flags are removed.
- Leave days are excluded from attendance days.
- Overtime, business trip, and leave counts are independent.

Manual UI validation:

- App opens to dashboard month calendar.
- Previous/today/next month commands work.
- Selecting a date updates the detail panel.
- Saving note and statuses persists after restart.
- Leave status shows a yellow dot.
- A date with note + leave shows both red and yellow dots.
- Monthly totals update after status changes.
- Light and dark themes remain legible.
- Narrow window behavior keeps calendar usable.

## Open Implementation Checks

- Confirm whether this machine has Visual Studio Windows App SDK templates or whether `dotnet` templates must be installed.
- Decide final packaging target: unpackaged exe, MSIX, or both.
- Decide whether to keep the existing Python app in the repository during migration or move it under a legacy folder after WinUI reaches parity.
