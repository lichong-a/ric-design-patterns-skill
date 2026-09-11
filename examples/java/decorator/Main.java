import java.util.*;
import java.util.function.*;

public final class Main {
    interface Text { String read(); }
    record PlainText(String value) implements Text {
        public String read() { return value; }
    }
    record PrefixText(Text inner) implements Text {
        public String read() { return "!" + inner.read(); }
    }
    record BracketText(Text inner) implements Text {
        public String read() { return "[" + inner.read() + "]"; }
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
        check(new BracketText(new PrefixText(new PlainText("hi"))).read().equals("[!hi]"));
        check(new PrefixText(new BracketText(new PlainText("hi"))).read().equals("![hi]"));
        System.out.println("OK decorator");
    }
}
