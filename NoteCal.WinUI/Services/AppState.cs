namespace NoteCal_WinUI.Services;

using NoteCal.Core.Models;
using NoteCal.Core.Services;

public sealed class AppState
{
    private readonly SortedSet<string> _selectedSummaryDates = new(StringComparer.Ordinal);
    private readonly SettingsRepository _settingsRepository = new();
    private AppSettings _settings = new();

    private AppState()
    {
        var now = DateTime.Now;
        CurrentYear = now.Year;
        CurrentMonth = now.Month;
    }

    public static AppState Current { get; } = new();

    public int CurrentYear { get; private set; }

    public int CurrentMonth { get; private set; }

    public IReadOnlyCollection<string> SelectedSummaryDates => _selectedSummaryDates;

    public AppSettings Settings => _settings;

    public async Task LoadAsync()
    {
        _settings = await _settingsRepository.LoadAsync(AppDataPaths.SettingsPath).ConfigureAwait(true);
        _selectedSummaryDates.Clear();
        foreach (var date in _settings.SummaryDateSelection)
        {
            _selectedSummaryDates.Add(date);
        }
    }

    public void SetCurrentMonth(int year, int month)
    {
        CurrentYear = year;
        CurrentMonth = month;
    }

    public void NavigateMonth(int delta)
    {
        var date = new DateOnly(CurrentYear, CurrentMonth, 1).AddMonths(delta);
        SetCurrentMonth(date.Year, date.Month);
    }

    public async Task ToggleSummaryDateAsync(string dateKey)
    {
        if (!_selectedSummaryDates.Add(dateKey))
        {
            _selectedSummaryDates.Remove(dateKey);
        }

        await SaveSettingsAsync().ConfigureAwait(true);
    }

    public async Task SetThemeAsync(string theme)
    {
        _settings.Theme = theme;
        await SaveSettingsAsync().ConfigureAwait(true);
    }

    public async Task SetShowLunarAsync(bool showLunar)
    {
        _settings.ShowLunar = showLunar;
        await SaveSettingsAsync().ConfigureAwait(true);
    }

    public async Task SetMinimizeToTrayAsync(bool minimizeToTray)
    {
        _settings.MinimizeToTray = minimizeToTray;
        await SaveSettingsAsync().ConfigureAwait(true);
    }

    public async Task ClearSummaryDatesAsync()
    {
        _selectedSummaryDates.Clear();
        await SaveSettingsAsync().ConfigureAwait(true);
    }

    public bool IsSummaryDateSelected(string dateKey)
    {
        return _selectedSummaryDates.Contains(dateKey);
    }

    private async Task SaveSettingsAsync()
    {
        _settings.SummaryDateSelection = _selectedSummaryDates.ToList();
        await _settingsRepository.SaveAsync(AppDataPaths.SettingsPath, _settings).ConfigureAwait(true);
    }
}
