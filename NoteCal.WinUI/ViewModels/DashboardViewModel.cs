using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Runtime.CompilerServices;
using NoteCal.Core.Models;
using NoteCal.Core.Services;
using NoteCal_WinUI.Services;

namespace NoteCal_WinUI.ViewModels;

public sealed class DashboardViewModel : INotifyPropertyChanged
{
    private readonly CalendarService _calendarService = new();
    private readonly LunarCalendarService _lunarCalendarService = new();
    private readonly AttendanceStatsService _statsService = new();
    private readonly NoteRepository _repository = new();
    private readonly SummaryService _summaryService = new();
    private readonly string _notesPath;
    private Dictionary<string, NoteEntry> _notes = new(StringComparer.Ordinal);
    private DateOnly _selectedDate;
    private string _selectedContent = string.Empty;
    private bool _selectedOvertime;
    private bool _selectedBusinessTrip;
    private bool _selectedLeave;
    private string _persistedSelectedContent = string.Empty;
    private bool _persistedSelectedOvertime;
    private bool _persistedSelectedBusinessTrip;
    private bool _persistedSelectedLeave;
    private bool _isSummarySelectionMode;

    public DashboardViewModel()
    {
        CurrentYear = AppState.Current.CurrentYear;
        CurrentMonth = AppState.Current.CurrentMonth;
        var today = DateOnly.FromDateTime(DateTime.Now);
        _selectedDate = today.Year == CurrentYear && today.Month == CurrentMonth
            ? today
            : new DateOnly(CurrentYear, CurrentMonth, 1);
        _notesPath = AppDataPaths.NotesPath;
    }

    public event PropertyChangedEventHandler? PropertyChanged;

    public ObservableCollection<DashboardDayViewModel> Days { get; } = [];

    public int CurrentYear { get; private set; }

    public int CurrentMonth { get; private set; }

    public string MonthTitle => $"{CurrentYear} 年 {CurrentMonth} 月";

    public string SelectedDateTitle => $"{_selectedDate:yyyy 年 M 月 d 日}";

    public string SelectedDateSubtitle
    {
        get
        {
            var flags = new List<string>();
            if (SelectedOvertime)
            {
                flags.Add("加班");
            }

            if (SelectedBusinessTrip)
            {
                flags.Add("出差");
            }

            if (SelectedLeave)
            {
                flags.Add("请假");
            }

            return flags.Count == 0 ? "未标记状态" : $"已标记：{string.Join(" / ", flags)}";
        }
    }

    public string SelectedContent
    {
        get => _selectedContent;
        set
        {
            if (_selectedContent != value)
            {
                _selectedContent = value;
                OnPropertyChanged();
                OnSelectedEditChanged();
            }
        }
    }

    public bool SelectedOvertime
    {
        get => _selectedOvertime;
        set
        {
            if (_selectedOvertime != value)
            {
                _selectedOvertime = value;
                OnPropertyChanged();
                OnPropertyChanged(nameof(SelectedDateSubtitle));
                OnSelectedEditChanged();
            }
        }
    }

    public bool SelectedBusinessTrip
    {
        get => _selectedBusinessTrip;
        set
        {
            if (_selectedBusinessTrip != value)
            {
                _selectedBusinessTrip = value;
                OnPropertyChanged();
                OnPropertyChanged(nameof(SelectedDateSubtitle));
                OnSelectedEditChanged();
            }
        }
    }

    public bool SelectedLeave
    {
        get => _selectedLeave;
        set
        {
            if (_selectedLeave != value)
            {
                _selectedLeave = value;
                OnPropertyChanged();
                OnPropertyChanged(nameof(SelectedDateSubtitle));
                OnSelectedEditChanged();
            }
        }
    }

    public bool IsSelectedDirty =>
        SelectedContent != _persistedSelectedContent
        || SelectedOvertime != _persistedSelectedOvertime
        || SelectedBusinessTrip != _persistedSelectedBusinessTrip
        || SelectedLeave != _persistedSelectedLeave;

    public string UnsavedStatus => IsSelectedDirty ? "有未保存更改，切换日期前会自动保存。" : "更改已保存。";

    public string SaveButtonLabel => IsSelectedDirty ? "保存更改" : "保存";

    public int AttendanceDays { get; private set; }

    public int OvertimeDays { get; private set; }

    public int BusinessTripDays { get; private set; }

    public int LeaveDays { get; private set; }

    public bool IsSummarySelectionMode
    {
        get => _isSummarySelectionMode;
        private set
        {
            if (_isSummarySelectionMode != value)
            {
                _isSummarySelectionMode = value;
                OnPropertyChanged();
                OnPropertyChanged(nameof(SummarySelectionButtonLabel));
                OnPropertyChanged(nameof(SummarySelectionStatus));
            }
        }
    }

    public string SummarySelectionButtonLabel => IsSummarySelectionMode ? "完成选择" : "选择日期";

    public string SummarySelectionStatus
    {
        get
        {
            var count = AppState.Current.SelectedSummaryDates.Count;
            if (!IsSummarySelectionMode && count == 0)
            {
                return "月历、统计和所选日期笔记";
            }

            return count == 0 ? "请选择要生成总结的日期" : $"已选择 {count} 天用于工作总结";
        }
    }

    public string SelectedSummaryDatesText => AppState.Current.SelectedSummaryDates.Count == 0
        ? "未选择日期"
        : string.Join("、", AppState.Current.SelectedSummaryDates);

    public async Task LoadAsync()
    {
        await AppState.Current.LoadAsync().ConfigureAwait(true);
        CurrentYear = AppState.Current.CurrentYear;
        CurrentMonth = AppState.Current.CurrentMonth;
        _notes = new Dictionary<string, NoteEntry>(
            await _repository.LoadAsync(_notesPath).ConfigureAwait(true),
            StringComparer.Ordinal);
        RefreshSelectedNote();
        RefreshCalendar();
    }

    public async Task SelectDateAsync(DashboardDayViewModel day)
    {
        if (day.Date is null)
        {
            return;
        }

        if (IsSummarySelectionMode)
        {
            await AppState.Current.ToggleSummaryDateAsync(day.DateKey).ConfigureAwait(true);
            OnPropertyChanged(nameof(SummarySelectionStatus));
            RefreshCalendar();
            return;
        }

        if (IsSelectedDirty)
        {
            await SaveSelectedAsync().ConfigureAwait(true);
        }

        _selectedDate = day.Date.Value;
        RefreshSelectedNote();
        RefreshCalendar();
    }

    public async Task PreviousMonthAsync()
    {
        if (IsSelectedDirty)
        {
            await SaveSelectedAsync().ConfigureAwait(true);
        }

        (CurrentYear, CurrentMonth) = _calendarService.NavigateMonth(CurrentYear, CurrentMonth, -1);
        AppState.Current.SetCurrentMonth(CurrentYear, CurrentMonth);
        SelectDefaultDateForCurrentMonth();
        RefreshSelectedNote();
        RefreshCalendar();
    }

    public async Task NextMonthAsync()
    {
        if (IsSelectedDirty)
        {
            await SaveSelectedAsync().ConfigureAwait(true);
        }

        (CurrentYear, CurrentMonth) = _calendarService.NavigateMonth(CurrentYear, CurrentMonth, 1);
        AppState.Current.SetCurrentMonth(CurrentYear, CurrentMonth);
        SelectDefaultDateForCurrentMonth();
        RefreshSelectedNote();
        RefreshCalendar();
    }

    public async Task GoToTodayAsync()
    {
        if (IsSelectedDirty)
        {
            await SaveSelectedAsync().ConfigureAwait(true);
        }

        var today = DateOnly.FromDateTime(DateTime.Now);
        CurrentYear = today.Year;
        CurrentMonth = today.Month;
        AppState.Current.SetCurrentMonth(CurrentYear, CurrentMonth);
        _selectedDate = today;
        RefreshSelectedNote();
        RefreshCalendar();
    }

    public void ToggleSummarySelectionMode()
    {
        IsSummarySelectionMode = !IsSummarySelectionMode;
        RefreshCalendar();
    }

    public async Task SaveSelectedAsync()
    {
        var key = _selectedDate.ToString("yyyy-MM-dd");
        var entry = new NoteEntry
        {
            Content = SelectedContent,
            Overtime = SelectedOvertime,
            BusinessTrip = SelectedBusinessTrip,
            Leave = SelectedLeave,
        };

        if (entry.HasAnyData)
        {
            _notes[key] = entry;
        }
        else
        {
            _notes.Remove(key);
        }

        await _repository.SaveAsync(_notesPath, _notes).ConfigureAwait(true);
        MarkSelectedPersisted();
        RefreshCalendar();
    }

    public async Task<string> BuildSelectedSummaryAsync()
    {
        if (IsSelectedDirty)
        {
            await SaveSelectedAsync().ConfigureAwait(true);
        }

        _notes = new Dictionary<string, NoteEntry>(
            await _repository.LoadAsync(_notesPath).ConfigureAwait(true),
            StringComparer.Ordinal);
        return _summaryService.BuildSummary(_notes, AppState.Current.SelectedSummaryDates);
    }

    public async Task ClearSelectedAsync()
    {
        SelectedContent = string.Empty;
        SelectedOvertime = false;
        SelectedBusinessTrip = false;
        SelectedLeave = false;
        _notes.Remove(_selectedDate.ToString("yyyy-MM-dd"));
        await _repository.SaveAsync(_notesPath, _notes).ConfigureAwait(true);
        MarkSelectedPersisted();
        RefreshCalendar();
    }

    private void SelectDefaultDateForCurrentMonth()
    {
        var today = DateOnly.FromDateTime(DateTime.Now);
        _selectedDate = today.Year == CurrentYear && today.Month == CurrentMonth
            ? today
            : new DateOnly(CurrentYear, CurrentMonth, 1);
    }

    private void RefreshSelectedNote()
    {
        if (_notes.TryGetValue(_selectedDate.ToString("yyyy-MM-dd"), out var entry))
        {
            _selectedContent = entry.Content;
            _selectedOvertime = entry.Overtime;
            _selectedBusinessTrip = entry.BusinessTrip;
            _selectedLeave = entry.Leave;
        }
        else
        {
            _selectedContent = string.Empty;
            _selectedOvertime = false;
            _selectedBusinessTrip = false;
            _selectedLeave = false;
        }

        MarkSelectedPersisted();
        OnPropertyChanged(nameof(SelectedDateTitle));
        OnPropertyChanged(nameof(SelectedDateSubtitle));
        OnPropertyChanged(nameof(SelectedContent));
        OnPropertyChanged(nameof(SelectedOvertime));
        OnPropertyChanged(nameof(SelectedBusinessTrip));
        OnPropertyChanged(nameof(SelectedLeave));
        OnSelectedEditChanged();
    }

    private void RefreshCalendar()
    {
        Days.Clear();
        var today = DateOnly.FromDateTime(DateTime.Now);
        var showLunar = AppState.Current.Settings.ShowLunar;
        var isDarkTheme = string.Equals(AppState.Current.Settings.Theme, "dark", StringComparison.OrdinalIgnoreCase);
        foreach (var day in _calendarService.GetMonthGrid(CurrentYear, CurrentMonth))
        {
            _notes.TryGetValue(day.DateKey, out var note);
            Days.Add(new DashboardDayViewModel(
                day,
                note,
                today,
                _selectedDate,
                AppState.Current.IsSummaryDateSelected(day.DateKey),
                showLunar && day.Date is not null ? _lunarCalendarService.GetLunarText(day.Date.Value) : string.Empty,
                isDarkTheme));
        }

        var stats = _statsService.CalculateMonth(CurrentYear, CurrentMonth, _notes);
        AttendanceDays = stats.AttendanceDays;
        OvertimeDays = stats.OvertimeDays;
        BusinessTripDays = stats.BusinessTripDays;
        LeaveDays = stats.LeaveDays;

        OnPropertyChanged(nameof(MonthTitle));
        OnPropertyChanged(nameof(AttendanceDays));
        OnPropertyChanged(nameof(OvertimeDays));
        OnPropertyChanged(nameof(BusinessTripDays));
        OnPropertyChanged(nameof(LeaveDays));
        OnPropertyChanged(nameof(SummarySelectionStatus));
        OnPropertyChanged(nameof(SelectedSummaryDatesText));
    }

    private void OnPropertyChanged([CallerMemberName] string? propertyName = null)
    {
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
    }

    private void MarkSelectedPersisted()
    {
        _persistedSelectedContent = _selectedContent;
        _persistedSelectedOvertime = _selectedOvertime;
        _persistedSelectedBusinessTrip = _selectedBusinessTrip;
        _persistedSelectedLeave = _selectedLeave;
        OnSelectedEditChanged();
    }

    private void OnSelectedEditChanged()
    {
        OnPropertyChanged(nameof(IsSelectedDirty));
        OnPropertyChanged(nameof(UnsavedStatus));
        OnPropertyChanged(nameof(SaveButtonLabel));
    }
}
