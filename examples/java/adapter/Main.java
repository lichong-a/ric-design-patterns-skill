import java.util.*;
import java.util.function.*;

public final class Main {
    interface Length { double meters(); }
    static final class LegacyMeter {
        double centimeters() { return 250.0; }
    }
    static final class MeterAdapter implements Length {
        private final LegacyMeter legacy;
        MeterAdapter(LegacyMeter legacy) { this.legacy = Objects.requireNonNull(legacy); }
        public double meters() { return legacy.centimeters() / 100.0; }
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
        Length length = new MeterAdapter(new LegacyMeter());
        check(length.meters() == 2.5);
        expectThrows(() -> new MeterAdapter(null));
        System.out.println("OK adapter");
    }
}
