import java.util.*;
import java.util.function.*;

public final class Main {
    static abstract class Importer {
        final String run(String raw) {
            String loaded = raw.trim();
            String parsed = parse(loaded);
            return "<" + parsed + ">";
        }
        protected abstract String parse(String text);
    }
    static final class UpperImporter extends Importer {
        protected String parse(String text) { return text.toUpperCase(Locale.ROOT); }
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
        check(new UpperImporter().run(" hello ").equals("<HELLO>"));
        System.out.println("OK template-method");
    }
}
