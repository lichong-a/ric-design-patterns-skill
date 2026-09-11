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

protocol Expr { func evaluate(_ context: [String: Int]) throws -> Int }
struct Literal: Expr {
    let value: Int
    func evaluate(_ context: [String: Int]) throws -> Int { value }
}
struct Variable: Expr {
    let name: String
    func evaluate(_ context: [String: Int]) throws -> Int {
        guard let value = context[name] else { throw DemoError.invalid("unknown variable") }
        return value
    }
}
struct Add: Expr {
    let left: any Expr
    let right: any Expr
    func evaluate(_ context: [String: Int]) throws -> Int {
        let a = try left.evaluate(context), b = try right.evaluate(context)
        let (sum, overflow) = a.addingReportingOverflow(b)
        guard !overflow else { throw DemoError.invalid("overflow") }
        return sum
    }
}

let expr = Add(left: Variable(name: "x"), right: Literal(value: 2))
let value = try expr.evaluate(["x": 3]); check(value == 5)
expectError { _ = try expr.evaluate([:]) }
expectError { _ = try Add(left: Literal(value: Int.max), right: Literal(value: 1)).evaluate([:]) }
print("OK interpreter")
