namespace NoteCal.Core.Models;

public sealed class CalendarDay
{
    public CalendarDay(DateOnly? date)
    {
        Date = date;
    }

    public DateOnly? Date { get; }

    public bool IsInMonth => Date is not null;

    public string DateKey => Date?.ToString("yyyy-MM-dd") ?? string.Empty;

    public string DayText => Date?.Day.ToString() ?? string.Empty;
}
