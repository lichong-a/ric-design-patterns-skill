import java.util.*;
import java.util.function.*;

public final class Main {
    static final class Editor {
        static final class Snapshot {
            private final Object owner;
            private final String text;
            private Snapshot(Object owner, String text) { this.owner = owner; this.text = text; }
        }
        private final Object owner = new Object();
        private String text;
        Editor(String text) { this.text = text; }
        String text() { return text; }
        void write(String value) { text = value; }
        Snapshot save() { return new Snapshot(owner, text); }
        void restore(Snapshot snapshot) {
            if (snapshot.owner != owner) throw new IllegalArgumentException("foreign snapshot");
            text = snapshot.text;
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
        var editor = new Editor("draft");
        var history = editor.save();
        editor.write("edited");
        editor.restore(history);
        check(editor.text().equals("draft"));
        expectThrows(() -> new Editor("other").restore(history));
        System.out.println("OK memento");
    }
}
