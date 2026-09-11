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

final class Counter { var value = 0 }
final class AddCommand {
    private let counter: Counter
    private let delta: Int
    private var before = 0
    private enum Phase { case new, done, undone }
    private var phase = Phase.new
    init(_ counter: Counter, delta: Int) { self.counter = counter; self.delta = delta }
    func execute() throws {
        guard phase == .new else { throw DemoError.invalid("execute once") }
        before = counter.value; counter.value += delta; phase = .done
    }
    func undo() throws {
        guard phase == .done else { throw DemoError.invalid("nothing to undo") }
        counter.value = before; phase = .undone
    }
}

let counter = Counter(); let command = AddCommand(counter, delta: 3)
expectError { try command.undo() }
try command.execute(); check(counter.value == 3)
expectError { try command.execute() }
try command.undo(); check(counter.value == 0)
expectError { try command.undo() }
print("OK command")
