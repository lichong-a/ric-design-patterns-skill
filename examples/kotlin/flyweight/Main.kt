package patterns.flyweight

fun expectError(action: () -> Unit) {
    var failed = false
    try { action() } catch (_: RuntimeException) { failed = true }
    check(failed)
}

data class Style(val font: String)
class StylePool {
    private val cache = mutableMapOf<String, Style>()
    fun get(font: String) = cache.getOrPut(font) { Style(font) }
}
data class Glyph(val character: Char, val x: Int, val style: Style)

fun main() {
    val pool = StylePool()
    val a = Glyph('a', 1, pool.get("mono"))
    val b = Glyph('b', 8, pool.get("mono"))
    check(a.style === b.style && a.x != b.x)
    check(pool.get("serif") !== a.style)
    println("OK flyweight")
}
