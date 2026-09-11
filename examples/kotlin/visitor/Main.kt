package patterns.visitor

fun expectError(action: () -> Unit) {
    var failed = false
    try { action() } catch (_: RuntimeException) { failed = true }
    check(failed)
}

interface NodeVisitor { fun visitText(node: TextNode): String; fun visitNumber(node: NumberNode): String }
interface Node { fun accept(visitor: NodeVisitor): String }
data class TextNode(val value: String) : Node { override fun accept(visitor: NodeVisitor) = visitor.visitText(this) }
data class NumberNode(val value: Int) : Node { override fun accept(visitor: NodeVisitor) = visitor.visitNumber(this) }
class RenderVisitor : NodeVisitor {
    override fun visitText(node: TextNode) = "text:${node.value}"
    override fun visitNumber(node: NumberNode) = "number:${node.value}"
}

fun main() {
    val visitor = RenderVisitor()
    check(TextNode("a").accept(visitor) == "text:a")
    check(NumberNode(7).accept(visitor) == "number:7")
    println("OK visitor")
}
