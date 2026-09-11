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

    public interface IText { string Render(); }
    public sealed class PlainText : IText { public string Render() => "hi"; }
    public sealed class PrefixText : IText
    {
        private readonly IText inner;
        public PrefixText(IText inner) { this.inner = inner ?? throw new ArgumentNullException(nameof(inner)); }
        public string Render() => "!" + inner.Render();
    }
    public sealed class BracketText : IText
    {
        private readonly IText inner;
        public BracketText(IText inner) { this.inner = inner ?? throw new ArgumentNullException(nameof(inner)); }
        public string Render() => "[" + inner.Render() + "]";
    }

    public static void Main()
    {
        Check(new BracketText(new PrefixText(new PlainText())).Render() == "[!hi]");
        Check(new PrefixText(new BracketText(new PlainText())).Render() == "![hi]");
        Console.WriteLine("OK decorator");
    }
}
