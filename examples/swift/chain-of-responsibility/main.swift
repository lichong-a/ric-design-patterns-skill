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

final class Rule {
    private let accepts: (Int) -> Bool
    private let next: Rule?
    init(_ accepts: @escaping (Int) -> Bool, next: Rule? = nil) { self.accepts = accepts; self.next = next }
    func handle(_ value: Int) -> Bool { accepts(value) && (next?.handle(value) ?? true) }
}

var visits = 0
let chain = Rule({ $0 > 0 }, next: Rule({ n in visits += 1; return n < 10 }))
check(!chain.handle(-1) && visits == 0)
check(chain.handle(5) && visits == 1)
check(!chain.handle(12) && visits == 2)
print("OK chain-of-responsibility")
