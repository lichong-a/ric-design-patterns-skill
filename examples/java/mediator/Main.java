import java.util.*;
import java.util.function.*;

public final class Main {
    static final class Toggle {
        private final Consumer<Boolean> changed;
        Toggle(Consumer<Boolean> changed) { this.changed = changed; }
        void select(boolean value) { changed.accept(value); }
    }
    static final class SubmitButton { boolean enabled; }
    static final class Dialog {
        final SubmitButton button = new SubmitButton();
        final Toggle toggle = new Toggle(this::changed);
        private void changed(boolean value) { button.enabled = value; }
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
        var dialog = new Dialog();
        check(!dialog.button.enabled);
        dialog.toggle.select(true);
        check(dialog.button.enabled);
        dialog.toggle.select(false);
        check(!dialog.button.enabled);
        System.out.println("OK mediator");
    }
}
