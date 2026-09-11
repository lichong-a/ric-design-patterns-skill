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

protocol Text { func render() -> String }
struct PlainText: Text { func render() -> String { "hi" } }
struct PrefixText: Text {
    let inner: any Text
    func render() -> String { "!" + inner.render() }
}
struct BracketText: Text {
    let inner: any Text
    func render() -> String { "[" + inner.render() + "]" }
}

check(BracketText(inner: PrefixText(inner: PlainText())).render() == "[!hi]")
check(PrefixText(inner: BracketText(inner: PlainText())).render() == "![hi]")
print("OK decorator")
