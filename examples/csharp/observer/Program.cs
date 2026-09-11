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

    public sealed class Events
    {
        private int sequence;
        private readonly Dictionary<int, Action<int>> listeners = new();
        public int Subscribe(Action<int> listener) { int token = ++sequence; listeners.Add(token, listener); return token; }
        public void Unsubscribe(int token) { listeners.Remove(token); }
        public void Emit(int value)
        {
            var snapshot = listeners.Values.ToArray();
            foreach (var listener in snapshot) listener(value);
        }
    }

    public static void Main()
    {
        var events = new Events(); var seen = new List<int>();
        int token = events.Subscribe(seen.Add);
        events.Emit(1); events.Unsubscribe(token); events.Emit(2);
        Check(seen.SequenceEqual(new[] { 1 }));
        int self = 0; self = events.Subscribe(_ => events.Unsubscribe(self));
        events.Emit(3); events.Emit(4);
        Console.WriteLine("OK observer");
    }
}
