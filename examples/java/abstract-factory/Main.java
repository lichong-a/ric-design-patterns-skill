import java.util.*;
import java.util.function.*;

public final class Main {
    interface Button { String draw(); }
    interface Checkbox { String mark(); }
    record ThemedButton(String theme) implements Button {
        public String draw() { return theme + ":button"; }
    }
    record ThemedCheckbox(String theme) implements Checkbox {
        public String mark() { return theme + ":checkbox"; }
    }
    interface WidgetFactory {
        Button button();
        Checkbox checkbox();
    }
    static final class LightFactory implements WidgetFactory {
        public Button button() { return new ThemedButton("light"); }
        public Checkbox checkbox() { return new ThemedCheckbox("light"); }
    }
    static final class DarkFactory implements WidgetFactory {
        public Button button() { return new ThemedButton("dark"); }
        public Checkbox checkbox() { return new ThemedCheckbox("dark"); }
    }
    static String screen(WidgetFactory factory) {
        return factory.button().draw() + "," + factory.checkbox().mark();
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
        check(screen(new LightFactory()).equals("light:button,light:checkbox"));
        check(screen(new DarkFactory()).equals("dark:button,dark:checkbox"));
        System.out.println("OK abstract-factory");
    }
}
