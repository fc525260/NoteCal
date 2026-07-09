namespace NoteCal.Core.Models;

public sealed class AppSettings
{
    public string Theme { get; set; } = "light";

    public bool MinimizeToTray { get; set; } = true;

    public bool ShowLunar { get; set; } = true;

    public List<string> SummaryDateSelection { get; set; } = [];
}
