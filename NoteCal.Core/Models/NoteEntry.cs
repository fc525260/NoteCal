namespace NoteCal.Core.Models;

public sealed class NoteEntry
{
    public string Content { get; set; } = string.Empty;

    public bool Overtime { get; set; }

    public bool BusinessTrip { get; set; }

    public bool Leave { get; set; }

    public bool HasContent => !string.IsNullOrWhiteSpace(Content);

    public bool HasAnyData => HasContent || Overtime || BusinessTrip || Leave;
}
