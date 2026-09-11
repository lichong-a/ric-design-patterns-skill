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

final class Settings: Sendable {
    static let shared = Settings()
    let mode = "demo"
    private init() {}
}

check(Settings.shared === Settings.shared)
check(Settings.shared.mode == "demo")
print("OK singleton")
