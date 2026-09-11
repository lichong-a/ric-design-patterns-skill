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

struct Bag: Sequence {
    let values: [Int]
    func makeIterator() -> IndexingIterator<[Int]> { values.makeIterator() }
}

let bag = Bag(values: [1, 2, 3])
var a = bag.makeIterator(), b = bag.makeIterator()
check(a.next() == 1 && a.next() == 2 && b.next() == 1)
check(Array(bag) == [1, 2, 3])
var empty = Bag(values: []).makeIterator(); check(empty.next() == nil)
print("OK iterator")
