import java.util.*;
import java.util.function.*;

public final class Main {
    static final class Counter { int value; }
    enum Phase { NEW, DONE, UNDONE }
    static final class AddCommand {
        private final Counter counter;
        private final int amount;
        private int before;
        private Phase phase = Phase.NEW;
        AddCommand(Counter counter, int amount) { this.counter = counter; this.amount = amount; }
        void execute() {
            if (phase != Phase.NEW) throw new IllegalStateException("already executed");
            before = counter.value;
            counter.value += amount;
            phase = Phase.DONE;
        }
        void undo() {
            if (phase != Phase.DONE) throw new IllegalStateException("nothing to undo");
            counter.value = before;
            phase = Phase.UNDONE;
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
        var counter = new Counter();
        var command = new AddCommand(counter, 5);
        command.execute();
        check(counter.value == 5);
        expectThrows(command::execute);
        command.undo();
        check(counter.value == 0);
        expectThrows(command::undo);
        System.out.println("OK command");
    }
}
