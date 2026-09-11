import java.util.*;
import java.util.function.*;

public final class Main {
    interface Image { String render(); }
    static final class RealImage implements Image {
        public String render() { return "pixels"; }
    }
    static final class ImageProxy implements Image {
        private RealImage real;
        int loads;
        public String render() {
            if (real == null) { real = new RealImage(); loads++; }
            return real.render();
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
        var proxy = new ImageProxy();
        check(proxy.loads == 0);
        check(proxy.render().equals("pixels"));
        check(proxy.render().equals("pixels"));
        check(proxy.loads == 1);
        System.out.println("OK proxy");
    }
}
