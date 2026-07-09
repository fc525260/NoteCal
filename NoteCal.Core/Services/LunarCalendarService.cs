using System.Globalization;

namespace NoteCal.Core.Services;

public sealed class LunarCalendarService
{
    private static readonly ChineseLunisolarCalendar Calendar = new();

    private static readonly string[] MonthNames =
    [
        "正月", "二月", "三月", "四月", "五月", "六月",
        "七月", "八月", "九月", "十月", "冬月", "腊月",
    ];

    private static readonly string[] DayNames =
    [
        "初一", "初二", "初三", "初四", "初五", "初六", "初七", "初八", "初九", "初十",
        "十一", "十二", "十三", "十四", "十五", "十六", "十七", "十八", "十九", "二十",
        "廿一", "廿二", "廿三", "廿四", "廿五", "廿六", "廿七", "廿八", "廿九", "三十",
    ];

    public string GetLunarText(DateOnly date)
    {
        var dateTime = date.ToDateTime(TimeOnly.MinValue);
        if (dateTime < Calendar.MinSupportedDateTime || dateTime > Calendar.MaxSupportedDateTime)
        {
            return string.Empty;
        }

        var year = Calendar.GetYear(dateTime);
        var month = Calendar.GetMonth(dateTime);
        var day = Calendar.GetDayOfMonth(dateTime);
        var leapMonth = Calendar.GetLeapMonth(year);
        var isLeapMonth = leapMonth > 0 && month == leapMonth;
        var normalizedMonth = leapMonth > 0 && month >= leapMonth ? month - 1 : month;

        if (normalizedMonth < 1 || normalizedMonth > MonthNames.Length || day < 1 || day > DayNames.Length)
        {
            return string.Empty;
        }

        var monthText = MonthNames[normalizedMonth - 1];
        return day == 1
            ? $"{(isLeapMonth ? "闰" : string.Empty)}{monthText}"
            : DayNames[day - 1];
    }
}
