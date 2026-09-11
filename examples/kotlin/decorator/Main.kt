package patterns.decorator

fun expectError(action: () -> Unit) {
    var failed = false
    try { action() } catch (_: RuntimeException) { failed = true }
    check(failed)
}

interface Text { fun render(): String }
class PlainText : Text { override fun render() = "hi" }
class PrefixText(private val inner: Text) : Text by inner {
    override fun render() = "!" + inner.render()
}
class BracketText(private val inner: Text) : Text by inner {
    override fun render() = "[" + inner.render() + "]"
}

fun main() {
    check(BracketText(PrefixText(PlainText())).render() == "[!hi]")
    check(PrefixText(BracketText(PlainText())).render() == "![hi]")
    println("OK decorator")
}
