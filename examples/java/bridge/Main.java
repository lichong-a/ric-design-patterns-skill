import java.util.*;
import java.util.function.*;

public final class Main {
    interface Channel { String send(String text); }
    static final class EmailChannel implements Channel {
        public String send(String text) { return "email:" + text; }
    }
    static final class SmsChannel implements Channel {
        public String send(String text) { return "sms:" + text; }
    }
    static class Notice {
        protected final Channel channel;
        Notice(Channel channel) { this.channel = Objects.requireNonNull(channel); }
        String send(String text) { return channel.send(text); }
    }
    static final class UrgentNotice extends Notice {
        UrgentNotice(Channel channel) { super(channel); }
        String send(String text) { return channel.send("!" + text); }
    }

    static void check(boolean condition) {
        if (!condition) throw new AssertionError("contract failed");
    }
    static void expectThrows(Runnable action) {
        boolean failed = false;
        try { action.run(); } catch (RuntimeException ex) { failed = true; }
        check(failed);
    }

    public static void main(String[] args) {
        check(new Notice(new EmailChannel()).send("ready").equals("email:ready"));
        check(new Notice(new SmsChannel()).send("ready").equals("sms:ready"));
        check(new UrgentNotice(new EmailChannel()).send("ready").equals("email:!ready"));
        check(new UrgentNotice(new SmsChannel()).send("ready").equals("sms:!ready"));
        System.out.println("OK bridge");
    }
}
