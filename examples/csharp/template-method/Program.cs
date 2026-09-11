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

    public abstract class Importer
    {
        protected abstract string Parse(string value);
        public string Run(string raw) => "<" + Parse(raw.Trim()) + ">";
    }
    public sealed class UpperImporter : Importer
    {
        protected override string Parse(string value) => value.ToUpperInvariant();
    }

    public static void Main()
    {
        Check(new UpperImporter().Run(" hello ") == "<HELLO>");
        Check(new UpperImporter().Run("   ") == "<>");
        Console.WriteLine("OK template-method");
    }
}
