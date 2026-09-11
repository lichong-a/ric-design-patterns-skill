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

    public sealed record Style(string Font);
    public sealed class StylePool
    {
        private readonly Dictionary<string, Style> cache = new(StringComparer.Ordinal);
        public Style Get(string font)
        {
            if (cache.TryGetValue(font, out var existing)) return existing;
            var created = new Style(font); cache.Add(font, created); return created;
        }
    }
    public sealed record Glyph(char Character, int X, Style Style);

    public static void Main()
    {
        var pool = new StylePool();
        var a = new Glyph('a', 1, pool.Get("mono")); var b = new Glyph('b', 8, pool.Get("mono"));
        Check(ReferenceEquals(a.Style, b.Style) && a.X != b.X);
        Check(!ReferenceEquals(pool.Get("serif"), a.Style));
        Console.WriteLine("OK flyweight");
    }
}
