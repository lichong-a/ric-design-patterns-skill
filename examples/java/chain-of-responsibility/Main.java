import java.util.*;
import java.util.function.*;

public final class Main {
    static final class Rule {
        private final IntPredicate predicate;
        private final Rule next;
        Rule(IntPredicate predicate, Rule next) { this.predicate = predicate; this.next = next; }
        boolean handle(int value) {
            if (!predicate.test(value)) return false;
            return next == null || next.handle(value);
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
        var visits = new ArrayList<Integer>();
        var chain = new Rule(n -> n > 0, new Rule(n -> { visits.add(n); return n < 1000; }, null));
        check(chain.handle(100));
        check(!chain.handle(-1));
        check(visits.equals(List.of(100)));
        check(!chain.handle(1000));
        System.out.println("OK chain-of-responsibility");
    }
}
