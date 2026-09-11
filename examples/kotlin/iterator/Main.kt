package patterns.iterator

fun expectError(action: () -> Unit) {
    var failed = false
    try { action() } catch (_: RuntimeException) { failed = true }
    check(failed)
}

class Bag(values: List<Int>) : Iterable<Int> {
    private val values = values.toList()
    override fun iterator(): Iterator<Int> = values.iterator()
}

fun main() {
    val bag = Bag(listOf(1, 2, 3))
    val a = bag.iterator(); val b = bag.iterator()
    check(a.next() == 1 && a.next() == 2 && b.next() == 1)
    check(bag.sum() == 6)
    check(!Bag(emptyList()).iterator().hasNext())
    println("OK iterator")
}
