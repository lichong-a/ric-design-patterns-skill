package patterns.factory_method

fun expectError(action: () -> Unit) {
    var failed = false
    try { action() } catch (_: RuntimeException) { failed = true }
    check(failed)
}

interface Renderer { fun render(): String }
class PlainRenderer : Renderer { override fun render() = "plain" }
class JsonRenderer : Renderer { override fun render() = "json" }
abstract class Publisher {
    protected abstract fun make(): Renderer
    fun publish() = "published:" + make().render()
}
class PlainPublisher : Publisher() { override fun make(): Renderer = PlainRenderer() }
class JsonPublisher : Publisher() { override fun make(): Renderer = JsonRenderer() }

fun main() {
    check(PlainPublisher().publish() == "published:plain")
    check(JsonPublisher().publish() == "published:json")
    println("OK factory-method")
}
