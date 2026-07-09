using Microsoft.UI;
using Microsoft.UI.Xaml;
using Microsoft.UI.Xaml.Media;
using NoteCal.Core.Models;

namespace NoteCal_WinUI.ViewModels;

public sealed class DashboardDayViewModel
{
    public DashboardDayViewModel(
        CalendarDay day,
        NoteEntry? note,
        DateOnly today,
        DateOnly? selectedDate,
        bool isMarkedForSummary)
        : this(day, note, today, selectedDate, isMarkedForSummary, string.Empty, isDarkTheme: false)
    {
    }

    public DashboardDayViewModel(
        CalendarDay day,
        NoteEntry? note,
        DateOnly today,
        DateOnly? selectedDate,
        bool isMarkedForSummary,
        bool showLunar)
        : this(day, note, today, selectedDate, isMarkedForSummary, showLunar ? string.Empty : string.Empty, isDarkTheme: false)
    {
    }

    public DashboardDayViewModel(
        CalendarDay day,
        NoteEntry? note,
        DateOnly today,
        DateOnly? selectedDate,
        bool isMarkedForSummary,
        string lunarText,
        bool isDarkTheme)
    {
        Date = day.Date;
        DayText = day.DayText;
        DateKey = day.DateKey;
        IsInMonth = day.IsInMonth;
        IsToday = Date == today;
        IsSelected = Date == selectedDate;
        IsMarkedForSummary = isMarkedForSummary;
        LunarText = IsInMonth ? lunarText : string.Empty;
        IsDarkTheme = isDarkTheme;

        if (note is not null)
        {
            HasNote = note.HasContent;
            Overtime = note.Overtime;
            BusinessTrip = note.BusinessTrip;
            Leave = note.Leave;
        }
    }

    public DateOnly? Date { get; }

    public string DayText { get; }

    public string DateKey { get; }

    public bool IsInMonth { get; }

    public bool IsToday { get; }

    public bool IsSelected { get; }

    public bool IsMarkedForSummary { get; }

    public bool IsDarkTheme { get; }

    public bool HasNote { get; }

    public bool Overtime { get; }

    public bool BusinessTrip { get; }

    public bool Leave { get; }

    public string LunarText { get; }

    public Visibility CellVisibility => IsInMonth ? Visibility.Visible : Visibility.Collapsed;

    public Visibility NoteDotVisibility => HasNote ? Visibility.Visible : Visibility.Collapsed;

    public Visibility OvertimeDotVisibility => Overtime ? Visibility.Visible : Visibility.Collapsed;

    public Visibility BusinessTripDotVisibility => BusinessTrip ? Visibility.Visible : Visibility.Collapsed;

    public Visibility LeaveDotVisibility => Leave ? Visibility.Visible : Visibility.Collapsed;

    public Brush CellBackground
    {
        get
        {
            if (IsToday)
            {
                return new SolidColorBrush(ColorHelper.FromArgb(255, 0, 103, 192));
            }

            return IsDarkTheme
                ? new SolidColorBrush(ColorHelper.FromArgb(96, 32, 32, 32))
                : new SolidColorBrush(Colors.White);
        }
    }

    public Brush CellBorderBrush
    {
        get
        {
            if (IsSelected || IsMarkedForSummary)
            {
                return new SolidColorBrush(ColorHelper.FromArgb(255, 0, 103, 192));
            }

            return IsDarkTheme
                ? new SolidColorBrush(ColorHelper.FromArgb(72, 255, 255, 255))
                : new SolidColorBrush(ColorHelper.FromArgb(32, 0, 0, 0));
        }
    }

    public Thickness CellBorderThickness => IsSelected || IsMarkedForSummary ? new Thickness(2) : new Thickness(1);

    public Brush PrimaryTextBrush => IsToday
        ? new SolidColorBrush(Colors.White)
        : IsDarkTheme
            ? new SolidColorBrush(ColorHelper.FromArgb(255, 245, 245, 245))
            : new SolidColorBrush(ColorHelper.FromArgb(255, 32, 32, 32));

    public Brush SecondaryTextBrush => IsToday
        ? new SolidColorBrush(ColorHelper.FromArgb(210, 255, 255, 255))
        : IsDarkTheme
            ? new SolidColorBrush(ColorHelper.FromArgb(210, 210, 210, 210))
            : new SolidColorBrush(ColorHelper.FromArgb(255, 100, 100, 100));
}
