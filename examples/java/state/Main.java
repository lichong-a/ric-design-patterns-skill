import java.util.*;
import java.util.function.*;

public final class Main {
    interface GateState {
        String name();
        GateState coin();
        GateState enter();
    }
    static final class Locked implements GateState {
        public String name() { return "locked"; }
        public GateState coin() { return new Unlocked(); }
        public GateState enter() { return this; }
    }
    static final class Unlocked implements GateState {
        public String name() { return "unlocked"; }
        public GateState coin() { return this; }
        public GateState enter() { return new Locked(); }
    }
    static final class Gate {
        private GateState state = new Locked();
        String name() { return state.name(); }
        void coin() { state = state.coin(); }
        void enter() { state = state.enter(); }
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
        var gate = new Gate();
        check(gate.name().equals("locked"));
        gate.enter();
        check(gate.name().equals("locked"));
        gate.coin();
        check(gate.name().equals("unlocked"));
        gate.enter();
        check(gate.name().equals("locked"));
        System.out.println("OK state");
    }
}
