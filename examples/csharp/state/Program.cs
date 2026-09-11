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

    public interface IGateState { bool IsOpen { get; } IGateState Coin(); IGateState Enter(); }
    public sealed class Locked : IGateState
    {
        public bool IsOpen => false;
        public IGateState Coin() => new Unlocked();
        public IGateState Enter() => this;
    }
    public sealed class Unlocked : IGateState
    {
        public bool IsOpen => true;
        public IGateState Coin() => this;
        public IGateState Enter() => new Locked();
    }
    public sealed class Gate
    {
        private IGateState state = new Locked();
        public bool IsOpen => state.IsOpen;
        public void Coin() { state = state.Coin(); }
        public void Enter() { state = state.Enter(); }
    }

    public static void Main()
    {
        var gate = new Gate(); Check(!gate.IsOpen);
        gate.Enter(); Check(!gate.IsOpen);
        gate.Coin(); Check(gate.IsOpen);
        gate.Coin(); Check(gate.IsOpen);
        gate.Enter(); Check(!gate.IsOpen);
        Console.WriteLine("OK state");
    }
}
