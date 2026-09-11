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

protocol GateState { var isOpen: Bool { get }; func coin() -> any GateState; func enter() -> any GateState }
struct Locked: GateState {
    let isOpen = false
    func coin() -> any GateState { Unlocked() }
    func enter() -> any GateState { self }
}
struct Unlocked: GateState {
    let isOpen = true
    func coin() -> any GateState { self }
    func enter() -> any GateState { Locked() }
}
final class Gate {
    private var state: any GateState = Locked()
    var isOpen: Bool { state.isOpen }
    func coin() { state = state.coin() }
    func enter() { state = state.enter() }
}

let gate = Gate(); check(!gate.isOpen)
gate.enter(); check(!gate.isOpen)
gate.coin(); check(gate.isOpen)
gate.coin(); check(gate.isOpen)
gate.enter(); check(!gate.isOpen)
print("OK state")
