import java.util.*;
import java.util.function.*;

public final class Main {
    interface Expr { int evaluate(Map<String, Integer> context); }
    record Literal(int value) implements Expr {
        public int evaluate(Map<String, Integer> context) { return value; }
    }
    record Variable(String name) implements Expr {
        public int evaluate(Map<String, Integer> context) {
            Integer value = context.get(name);
            if (value == null) throw new IllegalArgumentException("missing variable: " + name);
            return value;
        }
    }
    record Add(Expr left, Expr right) implements Expr {
        public int evaluate(Map<String, Integer> context) {
            return Math.addExact(left.evaluate(context), right.evaluate(context));
        }
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
        Expr expr = new Add(new Variable("x"), new Literal(2));
        check(expr.evaluate(Map.of("x", 3)) == 5);
        expectThrows(() -> expr.evaluate(Map.of()));
        expectThrows(() -> new Add(new Literal(Integer.MAX_VALUE), new Literal(1)).evaluate(Map.of()));
        System.out.println("OK interpreter");
    }
}
