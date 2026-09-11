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

    public interface IImage { string Read(); }
    public sealed class RealImage : IImage { public string Read() => "pixels"; }
    public sealed class LazyImage : IImage
    {
        private RealImage? real;
        public int Loads { get; private set; }
        public string Read()
        {
            if (real is null) { real = new RealImage(); Loads++; }
            return real.Read();
        }
    }

    public static void Main()
    {
        var image = new LazyImage(); Check(image.Loads == 0);
        Check(image.Read() == "pixels" && image.Read() == "pixels");
        Check(image.Loads == 1);
        Console.WriteLine("OK proxy");
    }
}
