package patterns.chain_of_responsibility

fun expectError(action: () -> Unit) {
    var failed = false
    try { action() } catch (_: RuntimeException) { failed = true }
    check(failed)
}

class Rule(private val accepts: (Int) -> Boolean, private val next: Rule? = null) {
    fun handle(value: Int): Boolean = accepts(value) && (next?.handle(value) ?: true)
}

fun main() {
    var visits = 0
    val chain = Rule({ it > 0 }, Rule({ visits++; it < 10 }))
    check(!chain.handle(-1) && visits == 0)
    check(chain.handle(5) && visits == 1)
    check(!chain.handle(12) && visits == 2)
    println("OK chain-of-responsibility")
}
