using System.Text;
using NoteCal.Core.Models;

namespace NoteCal.Core.Services;

public sealed class SummaryService
{
    public string BuildSummary(IReadOnlyDictionary<string, NoteEntry> notes)
    {
        return BuildSummary(notes, selectedDateKeys: null);
    }

    public string BuildSummary(
        IReadOnlyDictionary<string, NoteEntry> notes,
        IReadOnlyCollection<string>? selectedDateKeys)
    {
        var lines = new List<string>();
        var orderedNotes = notes
            .Where(note => note.Value.HasContent)
            .Where(note => selectedDateKeys is null || selectedDateKeys.Contains(note.Key))
            .OrderBy(note => note.Key, StringComparer.Ordinal)
            .ToList();

        for (var index = 0; index < orderedNotes.Count; index++)
        {
            var (date, entry) = orderedNotes[index];
            var ending = index == orderedNotes.Count - 1 ? "。" : ";";
            var dateLabel = date.Length >= 10 ? date[5..] : date;
            lines.Add($"{dateLabel}工作总结：{entry.Content.Trim()}{ending}");
        }

        return string.Join(Environment.NewLine, lines);
    }

    public string BuildStatusSummary(IReadOnlyDictionary<string, NoteEntry> notes)
    {
        var builder = new StringBuilder();
        foreach (var (date, entry) in notes.OrderBy(note => note.Key, StringComparer.Ordinal))
        {
            var flags = new List<string>();
            if (entry.Overtime)
            {
                flags.Add("加班");
            }

            if (entry.BusinessTrip)
            {
                flags.Add("出差");
            }

            if (entry.Leave)
            {
                flags.Add("请假");
            }

            if (flags.Count > 0)
            {
                builder.AppendLine($"{date}: {string.Join(" / ", flags)}");
            }
        }

        return builder.ToString().TrimEnd();
    }
}
