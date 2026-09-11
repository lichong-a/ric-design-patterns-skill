import java.util.*;
import java.util.function.*;

public final class Main {
    static final class Inventory {
        String reserve(int quantity) {
            if (quantity <= 0) throw new IllegalArgumentException("invalid quantity");
            return "reserved:" + quantity;
        }
    }
    static final class Receipts {
        String create(String reservation) { return "receipt:" + reservation; }
    }
    static final class Checkout {
        private final Inventory inventory;
        private final Receipts receipts;
        Checkout(Inventory inventory, Receipts receipts) {
            this.inventory = inventory; this.receipts = receipts;
        }
        String place(int quantity) { return receipts.create(inventory.reserve(quantity)); }
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
        var checkout = new Checkout(new Inventory(), new Receipts());
        check(checkout.place(2).equals("receipt:reserved:2"));
        expectThrows(() -> checkout.place(0));
        System.out.println("OK facade");
    }
}
