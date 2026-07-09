using System.ComponentModel;
using System.Runtime.CompilerServices;
using NoteCal.Core.Models;
using NoteCal.Core.Services;
using NoteCal_WinUI.Services;

namespace NoteCal_WinUI.ViewModels;

public sealed class StatsViewModel : INotifyPropertyChanged
{
    private readonly NoteRepository _repository = new();
    private readonly AttendanceStatsService _statsService = new();

    public event PropertyChangedEventHandler? PropertyChanged;

    public string MonthTitle { get; private set; } = string.Empty;

    public int AttendanceDays { get; private set; }

    public int OvertimeDays { get; private set; }

    public int BusinessTripDays { get; private set; }

    public int LeaveDays { get; private set; }

    public string OvertimeDates { get; private set; } = "无";

    public string BusinessTripDates { get; private set; } = "无";

    public string LeaveDates { get; private set; } = "无";

    public async Task LoadAsync()
    {
        await AppState.Current.LoadAsync().ConfigureAwait(true);
        var year = AppState.Current.CurrentYear;
        var month = AppState.Current.CurrentMonth;
        MonthTitle = $"{year} 年 {month} 月";
        var notes = await _repository.LoadAsync(AppDataPaths.NotesPath).ConfigureAwait(true);
        var stats = _statsService.CalculateMonth(year, month, notes);

        AttendanceDays = stats.AttendanceDays;
        OvertimeDays = stats.OvertimeDays;
        BusinessTripDays = stats.BusinessTripDays;
        LeaveDays = stats.LeaveDays;
        OvertimeDates = FormatDates(stats.OvertimeDates);
        BusinessTripDates = FormatDates(stats.BusinessTripDates);
        LeaveDates = FormatDates(stats.LeaveDates);

        OnPropertyChanged(string.Empty);
    }

    public async Task PreviousMonthAsync()
    {
        AppState.Current.NavigateMonth(-1);
        await LoadAsync();
    }

    public async Task NextMonthAsync()
    {
        AppState.Current.NavigateMonth(1);
        await LoadAsync();
    }

    public async Task CurrentMonthAsync()
    {
        var today = DateTime.Now;
        AppState.Current.SetCurrentMonth(today.Year, today.Month);
        await LoadAsync();
    }

    private static string FormatDates(IReadOnlyList<string> dates)
    {
        return dates.Count == 0 ? "无" : string.Join("、", dates);
    }

    private void OnPropertyChanged([CallerMemberName] string? propertyName = null)
    {
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
    }
}
