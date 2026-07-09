using NoteCal.Core.Models;

namespace NoteCal.Core.Services;

public sealed class CalendarService
{
    public IReadOnlyList<CalendarDay> GetMonthGrid(int year, int month)
    {
        var firstDay = new DateOnly(year, month, 1);
        var daysInMonth = DateTime.DaysInMonth(year, month);
        var leadingEmptyCells = ((int)firstDay.DayOfWeek + 6) % 7;

        var days = new List<CalendarDay>(42);
        for (var i = 0; i < leadingEmptyCells; i++)
        {
            days.Add(new CalendarDay(null));
        }

        for (var day = 1; day <= daysInMonth; day++)
        {
            days.Add(new CalendarDay(new DateOnly(year, month, day)));
        }

        while (days.Count < 42)
        {
            days.Add(new CalendarDay(null));
        }

        return days;
    }

    public (int Year, int Month) NavigateMonth(int year, int month, int delta)
    {
        var date = new DateOnly(year, month, 1).AddMonths(delta);
        return (date.Year, date.Month);
    }
}
