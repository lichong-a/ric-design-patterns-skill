import java.util.*;
import java.util.function.*;

public final class Main {
    static final class Pricing {
        private final IntUnaryOperator discount;
        Pricing(IntUnaryOperator discount) { this.discount = Objects.requireNonNull(discount); }
        int total(int base) {
            if (base < 0) throw new IllegalArgumentException("invalid base");
            return discount.applyAsInt(base);
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
        check(new Pricing(amount -> Math.max(0, amount - 10)).total(100) == 90);
        check(new Pricing(amount -> Math.max(0, amount - 20)).total(100) == 80);
        check(new Pricing(amount -> Math.max(0, amount - 20)).total(5) == 0);
        expectThrows(() -> new Pricing(amount -> amount).total(-1));
        System.out.println("OK strategy");
    }
}
