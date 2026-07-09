namespace NoteCal_WinUI.Services;

public static class AppDataPaths
{
    public static string AppRoot =>
        Environment.GetEnvironmentVariable("NOTECAL_PORTABLE_ROOT")
        ?? AppContext.BaseDirectory;

    public static string DataDirectory => Path.Combine(AppRoot, "user");

    public static string NotesPath => Path.Combine(DataDirectory, "NoteCal_notes.json");

    public static string SettingsPath => Path.Combine(DataDirectory, "NoteCal_settings.json");
}
