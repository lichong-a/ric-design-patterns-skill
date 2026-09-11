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

final class Style {
    let font: String
    init(_ font: String) { self.font = font }
}
final class StylePool {
    private var cache: [String: Style] = [:]
    func get(_ font: String) -> Style {
        if let cached = cache[font] { return cached }
        let created = Style(font); cache[font] = created; return created
    }
}
struct Glyph { let character: Character; let x: Int; let style: Style }

let pool = StylePool()
let a = Glyph(character: "a", x: 1, style: pool.get("mono"))
let b = Glyph(character: "b", x: 8, style: pool.get("mono"))
check(a.style === b.style && a.x != b.x)
check(pool.get("serif") !== a.style)
print("OK flyweight")
