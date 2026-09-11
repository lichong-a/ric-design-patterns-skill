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

    public sealed class Bag : IEnumerable<int>
    {
        private readonly int[] values;
        public Bag(IEnumerable<int> values) { this.values = values.ToArray(); }
        public IEnumerator<int> GetEnumerator() { foreach (int value in values) yield return value; }
        IEnumerator IEnumerable.GetEnumerator() => GetEnumerator();
    }

    public static void Main()
    {
        var bag = new Bag(new[] { 1, 2, 3 });
        using var a = bag.GetEnumerator(); using var b = bag.GetEnumerator();
        Check(a.MoveNext() && a.Current == 1);
        Check(a.MoveNext() && a.Current == 2);
        Check(b.MoveNext() && b.Current == 1);
        Check(bag.Sum() == 6 && !new Bag(Array.Empty<int>()).Any());
        Console.WriteLine("OK iterator");
    }
}
