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

    public sealed class Counter { public int Value { get; set; } }
    public sealed class AddCommand
    {
        private readonly Counter counter;
        private readonly int delta;
        private int before;
        private enum Phase { New, Done, Undone }
        private Phase phase = Phase.New;
        public AddCommand(Counter counter, int delta) { this.counter = counter; this.delta = delta; }
        public void Execute()
        {
            if (phase != Phase.New) throw new InvalidOperationException("execute once");
            before = counter.Value; counter.Value = checked(counter.Value + delta); phase = Phase.Done;
        }
        public void Undo()
        {
            if (phase != Phase.Done) throw new InvalidOperationException("nothing to undo");
            counter.Value = before; phase = Phase.Undone;
        }
    }

    public static void Main()
    {
        var counter = new Counter(); var command = new AddCommand(counter, 3);
        ExpectError(command.Undo);
        command.Execute(); Check(counter.Value == 3);
        ExpectError(command.Execute);
        command.Undo(); Check(counter.Value == 0);
        ExpectError(command.Undo);
        Console.WriteLine("OK command");
    }
}
