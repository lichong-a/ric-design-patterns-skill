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

final class Pricing {
    var rule: (Int) -> Int
    init(_ rule: @escaping (Int) -> Int) { self.rule = rule }
    func quote(_ base: Int) throws -> Int {
        guard base >= 0 else { throw DemoError.invalid("base") }
        return rule(base)
    }
}
func discount(_ amount: Int) -> (Int) -> Int { { base in max(0, base - amount) } }

let pricing = Pricing(discount(10))
let first = try pricing.quote(100); check(first == 90)
pricing.rule = discount(20)
let second = try pricing.quote(100), small = try pricing.quote(5)
check(second == 80 && small == 0)
expectError { _ = try pricing.quote(-1) }
print("OK strategy")
