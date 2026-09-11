package patterns.proxy

fun expectError(action: () -> Unit) {
    var failed = false
    try { action() } catch (_: RuntimeException) { failed = true }
    check(failed)
}

interface Image { fun read(): String }
class RealImage : Image { override fun read() = "pixels" }
class LazyImage : Image {
    var loads = 0
        private set
    private val real by lazy { loads++; RealImage() }
    override fun read() = real.read()
}

fun main() {
    val image = LazyImage()
    check(image.loads == 0)
    check(image.read() == "pixels" && image.read() == "pixels")
    check(image.loads == 1)
    println("OK proxy")
}
