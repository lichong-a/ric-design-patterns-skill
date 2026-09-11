package patterns.template_method

fun expectError(action: () -> Unit) {
    var failed = false
    try { action() } catch (_: RuntimeException) { failed = true }
    check(failed)
}

abstract class Importer {
    protected abstract fun parse(value: String): String
    fun run(raw: String): String = "<${parse(raw.trim())}>"
}
class UpperImporter : Importer() {
    override fun parse(value: String): String = value.uppercase(java.util.Locale.ROOT)
}

fun main() {
    check(UpperImporter().run(" hello ") == "<HELLO>")
    check(UpperImporter().run("   ") == "<>")
    println("OK template-method")
}
