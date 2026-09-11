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

struct Inventory {
    func reserve(_ quantity: Int) throws -> String {
        guard quantity > 0 else { throw DemoError.invalid("positive quantity required") }
        return "reserved:\(quantity)"
    }
}
struct Receipts { func create(_ reservation: String) -> String { "receipt:" + reservation } }
struct Checkout {
    let inventory: Inventory
    let receipts: Receipts
    func place(_ quantity: Int) throws -> String { receipts.create(try inventory.reserve(quantity)) }
}

let checkout = Checkout(inventory: Inventory(), receipts: Receipts())
let result = try checkout.place(2)
check(result == "receipt:reserved:2")
expectError { _ = try checkout.place(0) }
print("OK facade")
