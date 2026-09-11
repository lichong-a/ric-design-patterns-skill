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

    public interface IItem { int Total(); }
    public sealed class LineItem : IItem
    {
        private readonly int price;
        public LineItem(int price) { if (price < 0) throw new ArgumentException("price"); this.price = price; }
        public int Total() => price;
    }
    public sealed class Bundle : IItem
    {
        private readonly IItem[] children;
        public Bundle(IEnumerable<IItem> children) { this.children = children.ToArray(); }
        public int Total() => children.Sum(item => item.Total());
    }

    public static void Main()
    {
        var root = new Bundle(new IItem[] { new LineItem(10), new Bundle(new IItem[] { new LineItem(20), new LineItem(30) }) });
        Check(root.Total() == 60);
        Check(new Bundle(Array.Empty<IItem>()).Total() == 0);
        ExpectError(() => new LineItem(-1));
        Console.WriteLine("OK composite");
    }
}
