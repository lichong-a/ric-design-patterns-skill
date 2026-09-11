import java.util.*;
import java.util.function.*;

public final class Main {
    static final class Document {
        final List<List<String>> paragraphs;
        Document(List<List<String>> paragraphs) { this.paragraphs = paragraphs; }
        Document copy() {
            List<List<String>> rows = new ArrayList<>();
            for (var row : paragraphs) rows.add(new ArrayList<>(row));
            return new Document(rows);
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
        var original = new Document(new ArrayList<>(List.of(new ArrayList<>(List.of("draft")))));
        var copy = original.copy();
        copy.paragraphs.get(0).add("edited");
        check(original.paragraphs.get(0).equals(List.of("draft")));
        check(copy.paragraphs.get(0).size() == 2);
        check(copy != original);
        System.out.println("OK prototype");
    }
}
