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

class Importer {
    func parse(_ value: String) -> String { preconditionFailure("override parse") }
    final func run(_ raw: String) -> String {
        "<" + parse(raw.trimmingCharacters(in: .whitespacesAndNewlines)) + ">"
    }
}
final class UpperImporter: Importer {
    override func parse(_ value: String) -> String { value.uppercased() }
}

check(UpperImporter().run(" hello ") == "<HELLO>")
check(UpperImporter().run("   ") == "<>")
print("OK template-method")
