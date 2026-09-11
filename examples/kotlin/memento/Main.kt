package patterns.memento

fun expectError(action: () -> Unit) {
    var failed = false
    try { action() } catch (_: RuntimeException) { failed = true }
    check(failed)
}

interface Memento
class Editor {
    private data class Snapshot(val owner: Any, val text: String) : Memento
    private val owner = Any()
    var text = ""
    fun save(): Memento = Snapshot(owner, text)
    fun restore(memento: Memento) {
        val snapshot = memento as? Snapshot ?: error("invalid snapshot")
        require(snapshot.owner === owner) { "foreign snapshot" }
        text = snapshot.text
    }
}

fun main() {
    val a = Editor(); val b = Editor()
    a.text = "one"; val saved = a.save()
    a.text = "two"; a.restore(saved); check(a.text == "one")
    expectError { b.restore(saved) }
    println("OK memento")
}
