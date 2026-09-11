package patterns.facade

fun expectError(action: () -> Unit) {
    var failed = false
    try { action() } catch (_: RuntimeException) { failed = true }
    check(failed)
}

class Inventory {
    fun reserve(quantity: Int): String { require(quantity > 0); return "reserved:$quantity" }
}
class Receipts { fun create(reservation: String) = "receipt:$reservation" }
class Checkout(private val inventory: Inventory, private val receipts: Receipts) {
    fun place(quantity: Int) = receipts.create(inventory.reserve(quantity))
}

fun main() {
    val checkout = Checkout(Inventory(), Receipts())
    check(checkout.place(2) == "receipt:reserved:2")
    expectError { checkout.place(0) }
    println("OK facade")
}
