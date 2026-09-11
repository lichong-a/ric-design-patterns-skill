package patterns.abstract_factory

fun expectError(action: () -> Unit) {
    var failed = false
    try { action() } catch (_: RuntimeException) { failed = true }
    check(failed)
}

interface Button { fun draw(): String }
interface Checkbox { fun mark(): String }
class ThemedButton(private val theme: String) : Button { override fun draw() = "$theme:button" }
class ThemedCheckbox(private val theme: String) : Checkbox { override fun mark() = "$theme:checkbox" }
interface WidgetFactory { fun button(): Button; fun checkbox(): Checkbox }
class LightFactory : WidgetFactory {
    override fun button(): Button = ThemedButton("light")
    override fun checkbox(): Checkbox = ThemedCheckbox("light")
}
class DarkFactory : WidgetFactory {
    override fun button(): Button = ThemedButton("dark")
    override fun checkbox(): Checkbox = ThemedCheckbox("dark")
}
fun screen(f: WidgetFactory) = "${f.button().draw()}/${f.checkbox().mark()}"

fun main() {
    check(screen(LightFactory()) == "light:button/light:checkbox")
    check(screen(DarkFactory()) == "dark:button/dark:checkbox")
    println("OK abstract-factory")
}
