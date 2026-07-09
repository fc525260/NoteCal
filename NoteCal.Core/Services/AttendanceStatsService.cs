using NoteCal.Core.Models;

namespace NoteCal.Core.Services;

public sealed class AttendanceStatsService
{
    public AttendanceStats CalculateMonth(
        int year,
        int month,
        IReadOnlyDictionary<string, NoteEntry> notes)
    {
        var attendanceDays = 0;
        var overtimeDates = new List<string>();
        var businessTripDates = new List<string>();
        var leaveDates = new List<string>();
        var daysInMonth = DateTime.DaysInMonth(year, month);

        for (var day = 1; day <= daysInMonth; day++)
        {
            var date = new DateOnly(year, month, day);
            if (!notes.TryGetValue(date.ToString("yyyy-MM-dd"), out var entry))
            {
                continue;
            }

            if (entry.HasContent && !entry.Leave)
            {
                attendanceDays++;
            }

            var shortDate = date.ToString("MM-dd");
            if (entry.Overtime)
            {
                overtimeDates.Add(shortDate);
            }

            if (entry.BusinessTrip)
            {
                businessTripDates.Add(shortDate);
            }

            if (entry.Leave)
            {
                leaveDates.Add(shortDate);
            }
        }

        return new AttendanceStats
        {
            AttendanceDays = attendanceDays,
            OvertimeDays = overtimeDates.Count,
            BusinessTripDays = businessTripDates.Count,
            LeaveDays = leaveDates.Count,
            OvertimeDates = overtimeDates,
            BusinessTripDates = businessTripDates,
            LeaveDates = leaveDates,
        };
    }
}
