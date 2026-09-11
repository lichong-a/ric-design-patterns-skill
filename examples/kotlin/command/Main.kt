package patterns.command

fun expectError(action: () -> Unit) {
    var failed = false
    try { action() } catch (_: RuntimeException) { failed = true }
    check(failed)
}

data class Counter(var value: Int = 0)
class AddCommand(private val counter: Counter, private val delta: Int) {
    private enum class Phase { NEW, DONE, UNDONE }
    private var phase = Phase.NEW
    private var before = 0
    fun execute() {
        check(phase == Phase.NEW) { "execute once" }
        before = counter.value; counter.value += delta; phase = Phase.DONE
    }
    fun undo() {
        check(phase == Phase.DONE) { "nothing to undo" }
        counter.value = before; phase = Phase.UNDONE
    }
}

fun main() {
    val counter = Counter()
    val command = AddCommand(counter, 3)
    expectError { command.undo() }
    command.execute(); check(counter.value == 3)
    expectError { command.execute() }
    command.undo(); check(counter.value == 0)
    expectError { command.undo() }
    println("OK command")
}
