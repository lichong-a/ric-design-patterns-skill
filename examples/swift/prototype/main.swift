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

struct Document {
    var title: String
    var paragraphs: [[String]]
    func clone() -> Document { self }
}

let original = Document(title: "Design", paragraphs: [["one"]])
var copied = original.clone()
copied.paragraphs[0][0] = "changed"
copied.paragraphs[0].append("two")
check(original.paragraphs == [["one"]])
check(copied.paragraphs[0].count == 2)
print("OK prototype")
