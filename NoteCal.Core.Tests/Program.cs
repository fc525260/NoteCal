using NoteCal.Core.Models;
using NoteCal.Core.Services;

var tests = new List<(string Name, Func<Task> Test)>
{
    ("legacy string notes load as content-only", () => Run(LegacyStringNotesLoadAsContentOnly)),
    ("missing leave defaults to false", () => Run(MissingLeaveDefaultsToFalse)),
    ("leave days do not count as attendance", () => Run(LeaveDaysDoNotCountAsAttendance)),
    ("leave-only records are preserved", () => Run(LeaveOnlyRecordsArePreserved)),
    ("empty records with no flags are removed on save", () => Run(EmptyRecordsWithNoFlagsAreRemovedOnSave)),
    ("calendar grid is fixed six weeks", () => Run(CalendarGridIsFixedSixWeeks)),
    ("corrupted json is backed up before fallback", CorruptedJsonIsBackedUpBeforeFallback),
    ("summary uses sorted note content", () => Run(SummaryUsesSortedNoteContent)),
    ("summary can filter selected dates", () => Run(SummaryCanFilterSelectedDates)),
    ("settings preserve summary date selection", () => Run(SettingsPreserveSummaryDateSelection)),
    ("lunar calendar returns real date text", () => Run(LunarCalendarReturnsRealDateText)),
};

foreach (var (name, test) in tests)
{
    await test();
    Console.WriteLine($"PASS {name}");
}

Console.WriteLine($"{tests.Count} core tests passed.");

static Task Run(Action test)
{
    test();
    return Task.CompletedTask;
}

static void LegacyStringNotesLoadAsContentOnly()
{
    var repository = new NoteRepository();
    var notes = repository.LoadFromJson("""
        {
          "2026-07-01": "legacy note"
        }
        """);

    var note = notes["2026-07-01"];
    AssertEqual("legacy note", note.Content);
    AssertFalse(note.Overtime);
    AssertFalse(note.BusinessTrip);
    AssertFalse(note.Leave);
}

static void MissingLeaveDefaultsToFalse()
{
    var repository = new NoteRepository();
    var notes = repository.LoadFromJson("""
        {
          "2026-07-02": {
            "content": "normal work",
            "overtime": true,
            "business_trip": false
          }
        }
        """);

    var note = notes["2026-07-02"];
    AssertTrue(note.Overtime);
    AssertFalse(note.Leave);
}

static void LeaveDaysDoNotCountAsAttendance()
{
    var notes = new Dictionary<string, NoteEntry>
    {
        ["2026-07-01"] = new() { Content = "worked" },
        ["2026-07-02"] = new() { Content = "leave note", Leave = true },
        ["2026-07-03"] = new() { Leave = true },
        ["2026-07-04"] = new() { Overtime = true, BusinessTrip = true, Leave = true },
    };

    var stats = new AttendanceStatsService().CalculateMonth(2026, 7, notes);

    AssertEqual(1, stats.AttendanceDays);
    AssertEqual(1, stats.OvertimeDays);
    AssertEqual(1, stats.BusinessTripDays);
    AssertEqual(3, stats.LeaveDays);
}

static void LeaveOnlyRecordsArePreserved()
{
    var repository = new NoteRepository();
    var json = repository.SaveToJson(new Dictionary<string, NoteEntry>
    {
        ["2026-07-03"] = new() { Leave = true },
    });
    var loaded = repository.LoadFromJson(json);

    AssertTrue(loaded.ContainsKey("2026-07-03"));
    AssertTrue(loaded["2026-07-03"].Leave);
}

static void EmptyRecordsWithNoFlagsAreRemovedOnSave()
{
    var repository = new NoteRepository();
    var json = repository.SaveToJson(new Dictionary<string, NoteEntry>
    {
        ["2026-07-03"] = new(),
    });
    var loaded = repository.LoadFromJson(json);

    AssertFalse(loaded.ContainsKey("2026-07-03"));
}

static void CalendarGridIsFixedSixWeeks()
{
    var days = new CalendarService().GetMonthGrid(2026, 7);

    AssertEqual(42, days.Count);
    AssertEqual("2026-07-01", days.First(day => day.IsInMonth).DateKey);
    AssertEqual("2026-07-31", days.Last(day => day.IsInMonth).DateKey);
}

static async Task CorruptedJsonIsBackedUpBeforeFallback()
{
    var tempDir = Path.Combine(Path.GetTempPath(), $"notecal-core-tests-{Guid.NewGuid():N}");
    Directory.CreateDirectory(tempDir);
    var path = Path.Combine(tempDir, "NoteCal_notes.json");

    try
    {
        await File.WriteAllTextAsync(path, "{ broken json");
        var loaded = await new NoteRepository().LoadAsync(path);
        var backups = Directory.GetFiles(tempDir, "NoteCal_notes.json.*.bak");

        AssertEqual(0, loaded.Count);
        AssertEqual(1, backups.Length);
        AssertEqual("{ broken json", await File.ReadAllTextAsync(backups[0]));
    }
    finally
    {
        Directory.Delete(tempDir, recursive: true);
    }
}

static void SummaryUsesSortedNoteContent()
{
    var notes = new Dictionary<string, NoteEntry>
    {
        ["2026-07-03"] = new() { Content = "第三天" },
        ["2026-07-01"] = new() { Content = "第一天", Leave = true },
        ["2026-07-02"] = new() { Overtime = true },
    };

    var summary = new SummaryService().BuildSummary(notes);

    AssertEqual(
        $"07-01工作总结：第一天;{Environment.NewLine}07-03工作总结：第三天。",
        summary);
}

static void SummaryCanFilterSelectedDates()
{
    var notes = new Dictionary<string, NoteEntry>
    {
        ["2026-07-01"] = new() { Content = "第一天" },
        ["2026-07-02"] = new() { Content = "第二天" },
        ["2026-07-03"] = new() { Content = "第三天" },
    };

    var summary = new SummaryService().BuildSummary(notes, ["2026-07-02", "2026-07-03"]);

    AssertEqual(
        $"07-02工作总结：第二天;{Environment.NewLine}07-03工作总结：第三天。",
        summary);
}

static void SettingsPreserveSummaryDateSelection()
{
    var repository = new SettingsRepository();
    var settings = repository.LoadFromJson("""
        {
          "theme": "dark",
          "minimize_to_tray": false,
          "show_lunar": true,
          "summary_date_selection": ["2026-07-03", "2026-07-01", "2026-07-03"]
        }
        """);

    AssertEqual("dark", settings.Theme);
    AssertFalse(settings.MinimizeToTray);
    AssertEqual(2, settings.SummaryDateSelection.Count);
    AssertEqual("2026-07-01", settings.SummaryDateSelection[0]);
    AssertEqual("2026-07-03", settings.SummaryDateSelection[1]);

    var loaded = repository.LoadFromJson(repository.SaveToJson(settings));
    AssertEqual(2, loaded.SummaryDateSelection.Count);
    AssertEqual("2026-07-01", loaded.SummaryDateSelection[0]);
    AssertEqual("2026-07-03", loaded.SummaryDateSelection[1]);
}

static void LunarCalendarReturnsRealDateText()
{
    var service = new LunarCalendarService();

    AssertEqual("正月", service.GetLunarText(new DateOnly(2026, 2, 17)));
    AssertEqual("十五", service.GetLunarText(new DateOnly(2026, 3, 3)));
}

static void AssertEqual<T>(T expected, T actual)
{
    if (!EqualityComparer<T>.Default.Equals(expected, actual))
    {
        throw new InvalidOperationException($"Expected {expected}, got {actual}.");
    }
}

static void AssertTrue(bool condition)
{
    if (!condition)
    {
        throw new InvalidOperationException("Expected true.");
    }
}

static void AssertFalse(bool condition)
{
    if (condition)
    {
        throw new InvalidOperationException("Expected false.");
    }
}
