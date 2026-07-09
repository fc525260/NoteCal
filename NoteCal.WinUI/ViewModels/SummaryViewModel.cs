using System.ComponentModel;
using System.Runtime.CompilerServices;
using NoteCal.Core.Services;
using NoteCal_WinUI.Services;

namespace NoteCal_WinUI.ViewModels;

public sealed class SummaryViewModel : INotifyPropertyChanged
{
    private readonly NoteRepository _repository = new();
    private readonly SummaryService _summaryService = new();
    private string _summaryText = string.Empty;
    private int _selectedDateCount;

    public event PropertyChangedEventHandler? PropertyChanged;

    public string SummaryText
    {
        get => _summaryText;
        private set
        {
            if (_summaryText != value)
            {
                _summaryText = value;
                OnPropertyChanged();
                OnPropertyChanged(nameof(HasSummary));
                OnPropertyChanged(nameof(EmptyMessage));
            }
        }
    }

    public bool HasSummary => !string.IsNullOrWhiteSpace(SummaryText);

    public int SelectedDateCount
    {
        get => _selectedDateCount;
        private set
        {
            if (_selectedDateCount != value)
            {
                _selectedDateCount = value;
                OnPropertyChanged();
            }
        }
    }

    public string EmptyMessage => HasSummary
        ? $"已按日期排序生成总结，来源：{SelectedDateCount} 个所选日期。"
        : "当前没有可汇总的所选日期。请回到月历，点击“选择日期”后选择要汇总的日期。";

    public string SelectedDatesText { get; private set; } = "未选择日期";

    public async Task LoadAsync()
    {
        await AppState.Current.LoadAsync().ConfigureAwait(true);
        var notes = await _repository.LoadAsync(AppDataPaths.NotesPath).ConfigureAwait(true);
        var selectedDates = AppState.Current.SelectedSummaryDates;
        SelectedDateCount = selectedDates.Count;
        SelectedDatesText = selectedDates.Count == 0
            ? "未选择日期"
            : string.Join("、", selectedDates);
        SummaryText = _summaryService.BuildSummary(notes, selectedDates);
        OnPropertyChanged(nameof(SelectedDatesText));
    }

    public async Task ClearSelectionAsync()
    {
        await AppState.Current.ClearSummaryDatesAsync().ConfigureAwait(true);
        SelectedDateCount = 0;
        SelectedDatesText = "未选择日期";
        SummaryText = string.Empty;
        OnPropertyChanged(nameof(SelectedDatesText));
    }

    private void OnPropertyChanged([CallerMemberName] string? propertyName = null)
    {
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
    }
}
