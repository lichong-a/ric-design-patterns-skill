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

protocol Renderer { func render() -> String }
struct PlainRenderer: Renderer { func render() -> String { "plain" } }
struct JsonRenderer: Renderer { func render() -> String { "json" } }
class Publisher {
    func make() -> any Renderer { preconditionFailure("override make") }
    final func publish() -> String { "published:" + make().render() }
}
final class PlainPublisher: Publisher { override func make() -> any Renderer { PlainRenderer() } }
final class JsonPublisher: Publisher { override func make() -> any Renderer { JsonRenderer() } }

check(PlainPublisher().publish() == "published:plain")
check(JsonPublisher().publish() == "published:json")
print("OK factory-method")
