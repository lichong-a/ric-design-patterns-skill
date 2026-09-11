import java.util.*;
import java.util.function.*;

public final class Main {
    enum Settings {
        INSTANCE;
        final String mode = "production";
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
        check(Settings.INSTANCE == Settings.INSTANCE);
        check(Settings.INSTANCE.mode.equals("production"));
        System.out.println("OK singleton");
    }
}
