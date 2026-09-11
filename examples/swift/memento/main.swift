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

struct Snapshot {
    fileprivate let owner: AnyObject
    fileprivate let text: String
}
final class Editor {
    private final class Identity {}
    private let owner = Identity()
    var text = ""
    func save() -> Snapshot { Snapshot(owner: owner, text: text) }
    func restore(_ snapshot: Snapshot) throws {
        guard snapshot.owner === owner else { throw DemoError.invalid("foreign snapshot") }
        text = snapshot.text
    }
}

let a = Editor(), b = Editor()
a.text = "one"; let saved = a.save(); a.text = "two"
try a.restore(saved); check(a.text == "one")
expectError { try b.restore(saved) }
print("OK memento")
