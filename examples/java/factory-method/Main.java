import java.util.*;
import java.util.function.*;

public final class Main {
    interface Renderer { String render(); }
    static final class PlainRenderer implements Renderer {
        public String render() { return "plain"; }
    }
    static final class JsonRenderer implements Renderer {
        public String render() { return "{\"format\":\"json\"}"; }
    }
    static abstract class Publisher {
        protected abstract Renderer make();
        final String publish() { return "published:" + make().render(); }
    }
    static final class PlainPublisher extends Publisher {
        protected Renderer make() { return new PlainRenderer(); }
    }
    static final class JsonPublisher extends Publisher {
        protected Renderer make() { return new JsonRenderer(); }
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
        check(new PlainPublisher().publish().equals("published:plain"));
        check(new JsonPublisher().publish().equals("published:{\"format\":\"json\"}"));
        System.out.println("OK factory-method");
    }
}
