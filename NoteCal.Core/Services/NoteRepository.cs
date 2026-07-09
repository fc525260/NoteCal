using System.Text.Encodings.Web;
using System.Text.Json;
using System.Text.Json.Nodes;
using NoteCal.Core.Models;

namespace NoteCal.Core.Services;

public sealed class NoteRepository
{
    private static readonly JsonSerializerOptions WriteOptions = new()
    {
        Encoder = JavaScriptEncoder.UnsafeRelaxedJsonEscaping,
        WriteIndented = true,
    };

    public IReadOnlyDictionary<string, NoteEntry> LoadFromJson(string json)
    {
        if (string.IsNullOrWhiteSpace(json))
        {
            return new Dictionary<string, NoteEntry>();
        }

        var root = JsonNode.Parse(json)?.AsObject();
        if (root is null)
        {
            return new Dictionary<string, NoteEntry>();
        }

        var notes = new Dictionary<string, NoteEntry>(StringComparer.Ordinal);
        foreach (var item in root)
        {
            if (item.Value is null)
            {
                continue;
            }

            var entry = ParseEntry(item.Value);
            if (entry.HasAnyData)
            {
                notes[item.Key] = entry;
            }
        }

        return notes;
    }

    public async Task<IReadOnlyDictionary<string, NoteEntry>> LoadAsync(string path)
    {
        if (!File.Exists(path))
        {
            return new Dictionary<string, NoteEntry>();
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
            return new Dictionary<string, NoteEntry>();
        }
    }

    public string SaveToJson(IReadOnlyDictionary<string, NoteEntry> notes)
    {
        var serializable = notes
            .Where(note => note.Value.HasAnyData)
            .OrderBy(note => note.Key, StringComparer.Ordinal)
            .ToDictionary(
                note => note.Key,
                note => new
                {
                    content = note.Value.Content,
                    overtime = note.Value.Overtime,
                    business_trip = note.Value.BusinessTrip,
                    leave = note.Value.Leave,
                },
                StringComparer.Ordinal);

        return JsonSerializer.Serialize(serializable, WriteOptions);
    }

    public async Task SaveAsync(string path, IReadOnlyDictionary<string, NoteEntry> notes)
    {
        var directory = Path.GetDirectoryName(path);
        if (!string.IsNullOrEmpty(directory))
        {
            Directory.CreateDirectory(directory);
        }

        await File.WriteAllTextAsync(path, SaveToJson(notes)).ConfigureAwait(false);
    }

    private static NoteEntry ParseEntry(JsonNode node)
    {
        if (node.GetValueKind() == JsonValueKind.String)
        {
            return new NoteEntry { Content = node.GetValue<string>() };
        }

        var obj = node.AsObject();
        return new NoteEntry
        {
            Content = ReadString(obj, "content"),
            Overtime = ReadBool(obj, "overtime"),
            BusinessTrip = ReadBool(obj, "business_trip"),
            Leave = ReadBool(obj, "leave"),
        };
    }

    private static string ReadString(JsonObject obj, string key)
    {
        return obj.TryGetPropertyValue(key, out var value) && value is not null
            ? value.GetValue<string>()
            : string.Empty;
    }

    private static bool ReadBool(JsonObject obj, string key)
    {
        return obj.TryGetPropertyValue(key, out var value)
            && value is not null
            && value.GetValueKind() == JsonValueKind.True;
    }
}
