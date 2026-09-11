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

protocol Image { func read() -> String }
final class RealImage: Image { func read() -> String { "pixels" } }
final class LazyImage: Image {
    private var real: RealImage?
    private(set) var loads = 0
    func read() -> String {
        if let real { return real.read() }
        let created = RealImage(); real = created; loads += 1; return created.read()
    }
}

let image = LazyImage(); check(image.loads == 0)
check(image.read() == "pixels" && image.read() == "pixels")
check(image.loads == 1)
print("OK proxy")
