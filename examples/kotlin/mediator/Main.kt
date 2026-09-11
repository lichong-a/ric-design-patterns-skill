package patterns.mediator

fun expectError(action: () -> Unit) {
    var failed = false
    try { action() } catch (_: RuntimeException) { failed = true }
    check(failed)
}

class Toggle {
    var changed: ((Boolean) -> Unit)? = null
    fun set(enabled: Boolean) { changed?.invoke(enabled) }
}
class SubmitButton { var enabled = false }
class Dialog {
    val toggle = Toggle()
    val submit = SubmitButton()
    init { toggle.changed = { submit.enabled = it } }
}

fun main() {
    val dialog = Dialog()
    check(!dialog.submit.enabled)
    dialog.toggle.set(true); check(dialog.submit.enabled)
    dialog.toggle.set(false); check(!dialog.submit.enabled)
    println("OK mediator")
}
