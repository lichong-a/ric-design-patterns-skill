package patterns.composite

fun expectError(action: () -> Unit) {
    var failed = false
    try { action() } catch (_: RuntimeException) { failed = true }
    check(failed)
}

interface Item { fun total(): Int }
data class LineItem(private val price: Int) : Item {
    init { require(price >= 0) }
    override fun total() = price
}
class Bundle(children: List<Item>) : Item {
    private val children = children.toList()
    override fun total() = children.sumOf { it.total() }
}

fun main() {
    val root = Bundle(listOf(LineItem(10), Bundle(listOf(LineItem(20), LineItem(30)))))
    check(root.total() == 60)
    check(Bundle(emptyList()).total() == 0)
    expectError { LineItem(-1) }
    println("OK composite")
}
