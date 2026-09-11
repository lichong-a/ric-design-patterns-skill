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

    public sealed class Pricing
    {
        public Func<int, int> Rule { get; set; }
        public Pricing(Func<int, int> rule) { Rule = rule; }
        public int Quote(int value)
        {
            if (value < 0) throw new ArgumentException("base");
            return Rule(value);
        }
    }
    public static Func<int, int> Discount(int amount) => value => Math.Max(0, value - amount);

    public static void Main()
    {
        var pricing = new Pricing(Discount(10)); Check(pricing.Quote(100) == 90);
        pricing.Rule = Discount(20);
        Check(pricing.Quote(100) == 80 && pricing.Quote(5) == 0);
        ExpectError(() => pricing.Quote(-1));
        Console.WriteLine("OK strategy");
    }
}
