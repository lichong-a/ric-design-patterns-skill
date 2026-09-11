import java.util.*;
import java.util.function.*;

public final class Main {
    record Report(String title, List<String> sections) {
        Report { sections = List.copyOf(sections); }
    }
    static final class ReportBuilder {
        private String title = "";
        private final List<String> sections = new ArrayList<>();
        ReportBuilder title(String value) { title = value.trim(); return this; }
        ReportBuilder add(String section) { sections.add(section); return this; }
        Report build() {
            if (title.isEmpty()) throw new IllegalStateException("title is required");
            return new Report(title, sections);
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
        var builder = new ReportBuilder().title("Design").add("Intent");
        var report = builder.build();
        builder.add("Trade-offs");
        check(report.sections().equals(List.of("Intent")));
        expectThrows(() -> report.sections().add("bad"));
        expectThrows(() -> new ReportBuilder().build());
        System.out.println("OK builder");
    }
}
