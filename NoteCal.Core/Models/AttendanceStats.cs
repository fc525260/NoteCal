namespace NoteCal.Core.Models;

public sealed class AttendanceStats
{
    public int AttendanceDays { get; init; }

    public int OvertimeDays { get; init; }

    public int BusinessTripDays { get; init; }

    public int LeaveDays { get; init; }

    public IReadOnlyList<string> OvertimeDates { get; init; } = [];

    public IReadOnlyList<string> BusinessTripDates { get; init; } = [];

    public IReadOnlyList<string> LeaveDates { get; init; } = [];
}
