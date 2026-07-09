using System.Text.Encodings.Web;
using System.Text.Json;
using System.Text.Json.Nodes;
using NoteCal.Core.Models;

namespace NoteCal.Core.Services;

public sealed class SettingsRepository
{
    private static readonly JsonSerializerOptions WriteOptions = new()
    {
        Encoder = JavaScriptEncoder.UnsafeRelaxedJsonEscaping,
        WriteIndented = true,
    };

    public AppSettings LoadFromJson(string json)
    {
        var settings = new AppSettings();
        if (string.IsNullOrWhiteSpace(json))
        {
            return settings;
        }

        var root = JsonNode.Parse(json)?.AsObject();
        if (root is null)
        {
            return settings;
        }

        settings.Theme = ReadString(root, "theme", settings.Theme);
        settings.MinimizeToTray = ReadBool(root, "minimize_to_tray", settings.MinimizeToTray);
        settings.ShowLunar = ReadBool(root, "show_lunar", settings.ShowLunar);
        settings.SummaryDateSelection = ReadStringArray(root, "summary_date_selection")
            .Distinct(StringComparer.Ordinal)
            .OrderBy(value => value, StringComparer.Ordinal)
            .ToList();

        return settings;
    }

    public async Task<AppSettings> LoadAsync(string path)
    {
        if (!File.Exists(path))
        {
            return new AppSettings();
        }

        try
        {
            var json = await File.ReadAllTextAsync(path).ConfigureAwait(false);
            return LoadFromJson(json);
        }
        catch (JsonException)
        {
            var backupPath = $"{path}.{DateTime.Now:yyyyMMddHHmmss}.bak";
            File.Copy(path, backupPath, overwrite: false);
            return new AppSettings();
        }
    }

    public string SaveToJson(AppSettings settings)
    {
        var serializable = new
        {
            theme = settings.Theme,
            minimize_to_tray = settings.MinimizeToTray,
            show_lunar = settings.ShowLunar,
            summary_date_selection = settings.SummaryDateSelection
                .Distinct(StringComparer.Ordinal)
                .OrderBy(value => value, StringComparer.Ordinal)
                .ToArray(),
        };

        return JsonSerializer.Serialize(serializable, WriteOptions);
    }

    public async Task SaveAsync(string path, AppSettings settings)
    {
        var directory = Path.GetDirectoryName(path);
        if (!string.IsNullOrEmpty(directory))
        {
            Directory.CreateDirectory(directory);
        }

        await File.WriteAllTextAsync(path, SaveToJson(settings)).ConfigureAwait(false);
    }

    private static string ReadString(JsonObject obj, string key, string fallback)
    {
        return obj.TryGetPropertyValue(key, out var value) && value is not null
            ? value.GetValue<string>()
            : fallback;
    }

    private static bool ReadBool(JsonObject obj, string key, bool fallback)
    {
        if (!obj.TryGetPropertyValue(key, out var value) || value is null)
        {
            return fallback;
        }

        return value.GetValueKind() switch
        {
            JsonValueKind.True => true,
            JsonValueKind.False => false,
            _ => fallback,
        };
    }

    private static List<string> ReadStringArray(JsonObject obj, string key)
    {
        if (!obj.TryGetPropertyValue(key, out var value) || value is not JsonArray array)
        {
            return [];
        }

        return array
            .Where(item => item is not null && item.GetValueKind() == JsonValueKind.String)
            .Select(item => item!.GetValue<string>())
            .Where(item => !string.IsNullOrWhiteSpace(item))
            .ToList();
    }
}
