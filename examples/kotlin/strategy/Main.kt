package patterns.strategy

fun expectError(action: () -> Unit) {
    var failed = false
    try { action() } catch (_: RuntimeException) { failed = true }
    check(failed)
}

class Pricing(var rule: (Int) -> Int) {
    fun quote(base: Int): Int { require(base >= 0); return rule(base) }
}
fun discount(amount: Int): (Int) -> Int = { base -> (base - amount).coerceAtLeast(0) }

fun main() {
    val pricing = Pricing(discount(10))
    check(pricing.quote(100) == 90)
    pricing.rule = discount(20)
    check(pricing.quote(100) == 80 && pricing.quote(5) == 0)
    expectError { pricing.quote(-1) }
    println("OK strategy")
}
