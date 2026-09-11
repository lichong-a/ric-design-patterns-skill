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

    public sealed class Rule
    {
        private readonly Func<int, bool> accepts;
        private readonly Rule? next;
        public Rule(Func<int, bool> accepts, Rule? next = null) { this.accepts = accepts; this.next = next; }
        public bool Handle(int value) => accepts(value) && (next?.Handle(value) ?? true);
    }

    public static void Main()
    {
        int visits = 0;
        var chain = new Rule(n => n > 0, new Rule(n => { visits++; return n < 10; }));
        Check(!chain.Handle(-1) && visits == 0);
        Check(chain.Handle(5) && visits == 1);
        Check(!chain.Handle(12) && visits == 2);
        Console.WriteLine("OK chain-of-responsibility");
    }
}
