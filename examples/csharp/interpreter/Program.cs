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

    public interface IExpr { int Evaluate(IReadOnlyDictionary<string, int> context); }
    public sealed record Literal(int Value) : IExpr { public int Evaluate(IReadOnlyDictionary<string, int> context) => Value; }
    public sealed record Variable(string Name) : IExpr
    {
        public int Evaluate(IReadOnlyDictionary<string, int> context)
        {
            if (!context.TryGetValue(Name, out int value)) throw new ArgumentException("unknown variable");
            return value;
        }
    }
    public sealed record Add(IExpr Left, IExpr Right) : IExpr
    {
        public int Evaluate(IReadOnlyDictionary<string, int> context) => checked(Left.Evaluate(context) + Right.Evaluate(context));
    }

    public static void Main()
    {
        IExpr expr = new Add(new Variable("x"), new Literal(2));
        Check(expr.Evaluate(new Dictionary<string, int> { ["x"] = 3 }) == 5);
        ExpectError(() => expr.Evaluate(new Dictionary<string, int>()));
        ExpectError(() => new Add(new Literal(int.MaxValue), new Literal(1)).Evaluate(new Dictionary<string, int>()));
        Console.WriteLine("OK interpreter");
    }
}
