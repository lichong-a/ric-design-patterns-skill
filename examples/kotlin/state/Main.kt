package patterns.state

fun expectError(action: () -> Unit) {
    var failed = false
    try { action() } catch (_: RuntimeException) { failed = true }
    check(failed)
}

interface GateState {
    val open: Boolean
    fun coin(): GateState
    fun enter(): GateState
}
object Locked : GateState {
    override val open = false
    override fun coin(): GateState = Unlocked
    override fun enter(): GateState = this
}
object Unlocked : GateState {
    override val open = true
    override fun coin(): GateState = this
    override fun enter(): GateState = Locked
}
class Gate {
    private var state: GateState = Locked
    val open get() = state.open
    fun coin() { state = state.coin() }
    fun enter() { state = state.enter() }
}

fun main() {
    val gate = Gate(); check(!gate.open)
    gate.enter(); check(!gate.open)
    gate.coin(); check(gate.open)
    gate.coin(); check(gate.open)
    gate.enter(); check(!gate.open)
    println("OK state")
}
