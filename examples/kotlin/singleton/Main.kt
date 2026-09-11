package patterns.singleton

fun expectError(action: () -> Unit) {
    var failed = false
    try { action() } catch (_: RuntimeException) { failed = true }
    check(failed)
}

object Settings { val mode: String = "demo" }

fun main() {
    val a = Settings
    val b = Settings
    check(a === b && a.mode == "demo")
    println("OK singleton")
}
