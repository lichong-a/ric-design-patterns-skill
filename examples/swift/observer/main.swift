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

final class Events {
    private var sequence = 0
    private var listeners: [Int: (Int) -> Void] = [:]
    func subscribe(_ listener: @escaping (Int) -> Void) -> Int {
        sequence += 1; listeners[sequence] = listener; return sequence
    }
    func unsubscribe(_ token: Int) { listeners.removeValue(forKey: token) }
    func emit(_ value: Int) {
        let snapshot = Array(listeners.values)
        for listener in snapshot { listener(value) }
    }
}

let events = Events(); var seen: [Int] = []
let token = events.subscribe { seen.append($0) }
events.emit(1); events.unsubscribe(token); events.emit(2)
check(seen == [1])
var selfToken = 0
selfToken = events.subscribe { _ in events.unsubscribe(selfToken) }
events.emit(3); events.emit(4)
print("OK observer")
