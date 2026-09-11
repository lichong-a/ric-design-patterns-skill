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

    public interface IButton { string Draw(); }
    public interface ICheckbox { string Mark(); }
    public sealed record ThemedButton(string Theme) : IButton { public string Draw() => Theme + ":button"; }
    public sealed record ThemedCheckbox(string Theme) : ICheckbox { public string Mark() => Theme + ":checkbox"; }
    public interface IWidgetFactory { IButton Button(); ICheckbox Checkbox(); }
    public sealed class LightFactory : IWidgetFactory
    {
        public IButton Button() => new ThemedButton("light");
        public ICheckbox Checkbox() => new ThemedCheckbox("light");
    }
    public sealed class DarkFactory : IWidgetFactory
    {
        public IButton Button() => new ThemedButton("dark");
        public ICheckbox Checkbox() => new ThemedCheckbox("dark");
    }
    public static string Screen(IWidgetFactory f) => f.Button().Draw() + "/" + f.Checkbox().Mark();

    public static void Main()
    {
        Check(Screen(new LightFactory()) == "light:button/light:checkbox");
        Check(Screen(new DarkFactory()) == "dark:button/dark:checkbox");
        Console.WriteLine("OK abstract-factory");
    }
}
