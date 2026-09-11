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

    public sealed class Toggle
    {
        public event Action<bool>? Changed;
        public void Set(bool value) => Changed?.Invoke(value);
    }
    public sealed class SubmitButton { public bool Enabled { get; set; } }
    public sealed class Dialog : IDisposable
    {
        public Toggle Toggle { get; } = new();
        public SubmitButton Submit { get; } = new();
        public Dialog() { Toggle.Changed += OnChanged; }
        private void OnChanged(bool value) { Submit.Enabled = value; }
        public void Dispose() { Toggle.Changed -= OnChanged; }
    }

    public static void Main()
    {
        using var dialog = new Dialog(); Check(!dialog.Submit.Enabled);
        dialog.Toggle.Set(true); Check(dialog.Submit.Enabled);
        dialog.Toggle.Set(false); Check(!dialog.Submit.Enabled);
        dialog.Dispose(); dialog.Toggle.Set(true); Check(!dialog.Submit.Enabled);
        Console.WriteLine("OK mediator");
    }
}
