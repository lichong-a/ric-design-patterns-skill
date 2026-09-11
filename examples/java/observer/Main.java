import java.util.*;
import java.util.function.*;

public final class Main {
    static final class Events {
        private final Map<Integer, IntConsumer> listeners = new LinkedHashMap<>();
        private int next;
        int subscribe(IntConsumer listener) { listeners.put(++next, listener); return next; }
        void unsubscribe(int token) { listeners.remove(token); }
        void emit(int value) {
            for (var listener : List.copyOf(listeners.values())) listener.accept(value);
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
        var events = new Events();
        var seen = new ArrayList<Integer>();
        int token = events.subscribe(seen::add);
        events.emit(3);
        events.unsubscribe(token);
        events.emit(9);
        check(seen.equals(List.of(3)));
        var late = new ArrayList<Integer>();
        int other = events.subscribe(late::add);
        events.subscribe(value -> events.unsubscribe(other));
        events.emit(1);
        events.emit(2);
        check(late.equals(List.of(1)));
        System.out.println("OK observer");
    }
}
