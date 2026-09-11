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

    public interface IRenderer { string Render(); }
    public sealed class PlainRenderer : IRenderer { public string Render() => "plain"; }
    public sealed class JsonRenderer : IRenderer { public string Render() => "json"; }
    public abstract class Publisher
    {
        protected abstract IRenderer Make();
        public string Publish() => "published:" + Make().Render();
    }
    public sealed class PlainPublisher : Publisher { protected override IRenderer Make() => new PlainRenderer(); }
    public sealed class JsonPublisher : Publisher { protected override IRenderer Make() => new JsonRenderer(); }

    public static void Main()
    {
        Check(new PlainPublisher().Publish() == "published:plain");
        Check(new JsonPublisher().Publish() == "published:json");
        Console.WriteLine("OK factory-method");
    }
}
