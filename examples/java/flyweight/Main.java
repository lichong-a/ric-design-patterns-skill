import java.util.*;
import java.util.function.*;

public final class Main {
    record Style(String font) {}
    static final class StylePool {
        private final Map<String, Style> styles = new HashMap<>();
        Style get(String font) { return styles.computeIfAbsent(font, Style::new); }
    }
    record Glyph(String character, int x, Style style) {}

    static void check(boolean condition) {
        if (!condition) throw new AssertionError("contract failed");
    }
    static void expectThrows(Runnable action) {
        boolean failed = false;
        try { action.run(); } catch (RuntimeException ex) { failed = true; }
        check(failed);
    }

    public static void main(String[] args) {
        var pool = new StylePool();
        var a = new Glyph("a", 0, pool.get("mono"));
        var b = new Glyph("b", 10, pool.get("mono"));
        check(a.style() == b.style());
        check(a.x() != b.x());
        check(pool.get("serif") != a.style());
        System.out.println("OK flyweight");
    }
}
