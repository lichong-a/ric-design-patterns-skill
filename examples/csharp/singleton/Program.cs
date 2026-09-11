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

    public sealed class Settings
    {
        private static readonly Lazy<Settings> instance = new(() => new Settings());
        private Settings() { }
        public static Settings Instance => instance.Value;
        public string Mode => "demo";
    }

    public static void Main()
    {
        Check(ReferenceEquals(Settings.Instance, Settings.Instance));
        Check(Settings.Instance.Mode == "demo");
        Console.WriteLine("OK singleton");
    }
}
