import java.util.*;
import java.util.function.*;

public final class Main {
    interface Item { int total(); }
    record LineItem(int value) implements Item {
        public int total() { return value; }
    }
    record Bundle(List<Item> children) implements Item {
        Bundle { children = List.copyOf(children); }
        public int total() { return children.stream().mapToInt(Item::total).sum(); }
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
        Item root = new Bundle(List.of(new LineItem(10), new Bundle(List.of(new LineItem(20), new LineItem(30)))));
        check(root.total() == 60);
        check(new Bundle(List.of()).total() == 0);
        System.out.println("OK composite");
    }
}
