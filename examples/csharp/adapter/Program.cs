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

    public sealed class LegacySensor { public int Centimeters() => 250; }
    public interface IMeterReader { double Meters(); }
    public sealed class SensorAdapter : IMeterReader
    {
        private readonly LegacySensor sensor;
        public SensorAdapter(LegacySensor sensor) { this.sensor = sensor ?? throw new ArgumentNullException(nameof(sensor)); }
        public double Meters() => sensor.Centimeters() / 100.0;
    }

    public static void Main()
    {
        IMeterReader reader = new SensorAdapter(new LegacySensor());
        Check(reader.Meters() == 2.5);
        ExpectError(() => new SensorAdapter(null!));
        Console.WriteLine("OK adapter");
    }
}
