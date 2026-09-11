import Foundation

func check(_ condition: @autoclosure () -> Bool) {
    precondition(condition(), "check failed")
}
enum DemoError: Error { case invalid(String) }
func expectError(_ action: () throws -> Void) {
    var failed = false
    do { try action() } catch { failed = true }
    check(failed)
}

protocol Button { func draw() -> String }
protocol Checkbox { func mark() -> String }
struct ThemedButton: Button {
    let theme: String
    func draw() -> String { theme + ":button" }
}
struct ThemedCheckbox: Checkbox {
    let theme: String
    func mark() -> String { theme + ":checkbox" }
}
protocol WidgetFactory { func button() -> any Button; func checkbox() -> any Checkbox }
struct LightFactory: WidgetFactory {
    func button() -> any Button { ThemedButton(theme: "light") }
    func checkbox() -> any Checkbox { ThemedCheckbox(theme: "light") }
}
struct DarkFactory: WidgetFactory {
    func button() -> any Button { ThemedButton(theme: "dark") }
    func checkbox() -> any Checkbox { ThemedCheckbox(theme: "dark") }
}
func screen(_ f: any WidgetFactory) -> String { f.button().draw() + "/" + f.checkbox().mark() }

check(screen(LightFactory()) == "light:button/light:checkbox")
check(screen(DarkFactory()) == "dark:button/dark:checkbox")
print("OK abstract-factory")
