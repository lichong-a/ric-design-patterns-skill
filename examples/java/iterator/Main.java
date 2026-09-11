import java.util.*;
import java.util.function.*;

public final class Main {
    static final class Bag implements Iterable<Integer> {
        private final List<Integer> values;
        Bag(List<Integer> values) { this.values = List.copyOf(values); }
        public Iterator<Integer> iterator() { return values.iterator(); }
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
        var bag = new Bag(List.of(1, 2, 3));
        var a = bag.iterator();
        var b = bag.iterator();
        check(a.next() == 1);
        check(a.next() == 2);
        check(b.next() == 1);
        var seen = new ArrayList<Integer>();
        for (int value : bag) seen.add(value);
        check(seen.equals(List.of(1, 2, 3)));
        check(!new Bag(List.of()).iterator().hasNext());
        System.out.println("OK iterator");
    }
}
