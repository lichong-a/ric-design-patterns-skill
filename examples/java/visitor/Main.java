import java.util.*;
import java.util.function.*;

public final class Main {
    interface NodeVisitor {
        String visitText(TextNode node);
        String visitNumber(NumberNode node);
    }
    interface Node { String accept(NodeVisitor visitor); }
    record TextNode(String value) implements Node {
        public String accept(NodeVisitor visitor) { return visitor.visitText(this); }
    }
    record NumberNode(int value) implements Node {
        public String accept(NodeVisitor visitor) { return visitor.visitNumber(this); }
    }
    static final class RenderVisitor implements NodeVisitor {
        public String visitText(TextNode node) { return "text:" + node.value(); }
        public String visitNumber(NumberNode node) { return "number:" + node.value(); }
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
        var visitor = new RenderVisitor();
        List<Node> nodes = List.of(new TextNode("a"), new NumberNode(7));
        check(nodes.stream().map(node -> node.accept(visitor)).toList().equals(List.of("text:a", "number:7")));
        System.out.println("OK visitor");
    }
}
