package patterns.interpreter

fun expectError(action: () -> Unit) {
    var failed = false
    try { action() } catch (_: RuntimeException) { failed = true }
    check(failed)
}

interface Expr { fun eval(context: Map<String, Int>): Int }
data class Literal(val value: Int) : Expr { override fun eval(context: Map<String, Int>) = value }
data class Variable(val name: String) : Expr {
    override fun eval(context: Map<String, Int>) = requireNotNull(context[name]) { "unknown variable: $name" }
}
data class Add(val left: Expr, val right: Expr) : Expr {
    override fun eval(context: Map<String, Int>) = Math.addExact(left.eval(context), right.eval(context))
}

fun main() {
    val expr: Expr = Add(Variable("x"), Literal(2))
    check(expr.eval(mapOf("x" to 3)) == 5)
    expectError { expr.eval(emptyMap()) }
    expectError { Add(Literal(Int.MAX_VALUE), Literal(1)).eval(emptyMap()) }
    println("OK interpreter")
}
