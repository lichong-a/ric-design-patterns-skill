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

final class Toggle {
    var changed: ((Bool) -> Void)?
    func set(_ value: Bool) { changed?(value) }
}
final class SubmitButton { var enabled = false }
final class Dialog {
    let toggle = Toggle()
    let submit = SubmitButton()
    init() {
        toggle.changed = { [weak self] value in self?.submit.enabled = value }
    }
}

let dialog = Dialog(); check(!dialog.submit.enabled)
dialog.toggle.set(true); check(dialog.submit.enabled)
dialog.toggle.set(false); check(!dialog.submit.enabled)
print("OK mediator")
