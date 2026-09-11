package patterns.prototype

fun expectError(action: () -> Unit) {
    var failed = false
    try { action() } catch (_: RuntimeException) { failed = true }
    check(failed)
}

data class Document(val title: String, val paragraphs: MutableList<MutableList<String>>) {
    fun deepCopy() = copy(paragraphs = paragraphs.map { it.toMutableList() }.toMutableList())
}

fun main() {
    val original = Document("Design", mutableListOf(mutableListOf("one")))
    val copied = original.deepCopy()
    copied.paragraphs[0].add("two")
    check(original.paragraphs[0] == listOf("one"))
    check(copied.paragraphs[0].size == 2)
    println("OK prototype")
}
