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

    public sealed class Document
    {
        public string Title { get; }
        public List<List<string>> Paragraphs { get; }
        public Document(string title, List<List<string>> paragraphs) { Title = title; Paragraphs = paragraphs; }
        public Document DeepCopy() => new(Title, Paragraphs.Select(row => new List<string>(row)).ToList());
    }

    public static void Main()
    {
        var original = new Document("Design", new() { new() { "one" } });
        var copy = original.DeepCopy();
        copy.Paragraphs[0][0] = "changed"; copy.Paragraphs[0].Add("two");
        Check(original.Paragraphs[0].SequenceEqual(new[] { "one" }));
        Check(copy.Paragraphs[0].Count == 2);
        Console.WriteLine("OK prototype");
    }
}
