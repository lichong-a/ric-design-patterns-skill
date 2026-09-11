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

    public interface IChannel { string Send(string value); }
    public sealed class EmailChannel : IChannel { public string Send(string value) => "email:" + value; }
    public sealed class SmsChannel : IChannel { public string Send(string value) => "sms:" + value; }
    public class Notice
    {
        protected readonly IChannel Channel;
        public Notice(IChannel channel) { Channel = channel ?? throw new ArgumentNullException(nameof(channel)); }
        public virtual string Deliver(string value) => Channel.Send(value);
    }
    public sealed class UrgentNotice : Notice
    {
        public UrgentNotice(IChannel channel) : base(channel) { }
        public override string Deliver(string value) => Channel.Send("!" + value);
    }

    public static void Main()
    {
        Check(new Notice(new EmailChannel()).Deliver("hi") == "email:hi");
        Check(new UrgentNotice(new SmsChannel()).Deliver("hi") == "sms:!hi");
        Console.WriteLine("OK bridge");
    }
}
