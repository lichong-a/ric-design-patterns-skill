package patterns.observer

fun expectError(action: () -> Unit) {
    var failed = false
    try { action() } catch (_: RuntimeException) { failed = true }
    check(failed)
}

class Events {
    private var sequence = 0
    private val listeners = linkedMapOf<Int, (Int) -> Unit>()
    fun subscribe(listener: (Int) -> Unit): Int {
        val token = ++sequence; listeners[token] = listener; return token
    }
    fun unsubscribe(token: Int) { listeners.remove(token) }
    fun emit(value: Int) { listeners.values.toList().forEach { it(value) } }
}

fun main() {
    val events = Events(); val seen = mutableListOf<Int>()
    val token = events.subscribe { seen.add(it) }
    events.emit(1); events.unsubscribe(token); events.emit(2)
    check(seen == listOf(1))
    var self = 0; self = events.subscribe { events.unsubscribe(self) }
    events.emit(3); events.emit(4)
    println("OK observer")
}
