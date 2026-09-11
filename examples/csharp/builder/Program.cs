using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;

public static class Program
{
    private static void Check(bool condition)
    {
        if (!condition) throw new InvalidOperationException("check failed");
    }
    private static void ExpectError(Action action)
    {
        bool failed = false;
        try { action(); } catch (ArgumentException) { failed = true; }
        catch (InvalidOperationException) { failed = true; }
        catch (OverflowException) { failed = true; }
        Check(failed);
    }

    public sealed record Report(string Title, IReadOnlyList<string> Sections);
    public sealed class ReportBuilder
    {
        private string title = "";
        private readonly List<string> sections = new();
        public ReportBuilder Title(string value) { title = value.Trim(); return this; }
        public ReportBuilder Section(string value) { sections.Add(value); return this; }
        public Report Build()
        {
            if (title.Length == 0) throw new ArgumentException("title required");
            return new Report(title, Array.AsReadOnly(sections.ToArray()));
        }
    }

    public static void Main()
    {
        var builder = new ReportBuilder();
        ExpectError(() => builder.Build());
        var first = builder.Title("Design").Section("Intent").Build();
        builder.Section("Tests");
        Check(first.Sections.Count == 1 && first.Sections[0] == "Intent");
        Check(builder.Build().Sections.Count == 2);
        Console.WriteLine("OK builder");
    }
}
