package patterns.builder

fun expectError(action: () -> Unit) {
    var failed = false
    try { action() } catch (_: RuntimeException) { failed = true }
    check(failed)
}

data class Report(val title: String, val sections: List<String>)
class ReportBuilder {
    private var title = ""
    private val sections = mutableListOf<String>()
    fun title(value: String) = apply { title = value.trim() }
    fun section(value: String) = apply { sections.add(value) }
    fun build(): Report {
        require(title.isNotEmpty()) { "title required" }
        return Report(title, sections.toList())
    }
}

fun main() {
    val b = ReportBuilder()
    expectError { b.build() }
    val first = b.title("Design").section("Intent").build()
    b.section("Tests")
    check(first.sections == listOf("Intent"))
    check(b.build().sections.size == 2)
    println("OK builder")
}
