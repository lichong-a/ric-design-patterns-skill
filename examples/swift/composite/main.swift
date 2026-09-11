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

protocol Item { func total() -> Int }
struct LineItem: Item {
    let price: Int
    init(_ price: Int) throws {
        guard price >= 0 else { throw DemoError.invalid("price") }
        self.price = price
    }
    func total() -> Int { price }
}
struct Bundle: Item {
    let children: [any Item]
    func total() -> Int { children.reduce(0) { $0 + $1.total() } }
}

let root = Bundle(children: [try LineItem(10), Bundle(children: [try LineItem(20), try LineItem(30)])])
check(root.total() == 60 && Bundle(children: []).total() == 0)
expectError { _ = try LineItem(-1) }
print("OK composite")
