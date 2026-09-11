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

    public interface IMemento { }
    public sealed class Editor
    {
        private sealed record Snapshot(object Owner, string Text) : IMemento;
        private readonly object owner = new();
        public string Text { get; set; } = "";
        public IMemento Save() => new Snapshot(owner, Text);
        public void Restore(IMemento memento)
        {
            if (memento is not Snapshot snapshot || !ReferenceEquals(snapshot.Owner, owner))
                throw new ArgumentException("foreign snapshot");
            Text = snapshot.Text;
        }
    }

    public static void Main()
    {
        var a = new Editor(); var b = new Editor();
        a.Text = "one"; IMemento saved = a.Save(); a.Text = "two";
        a.Restore(saved); Check(a.Text == "one");
        ExpectError(() => b.Restore(saved));
        Console.WriteLine("OK memento");
    }
}
