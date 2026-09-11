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

struct Report { let title: String; let sections: [String] }
final class ReportBuilder {
    private var titleValue = ""
    private var sections: [String] = []
    @discardableResult func title(_ value: String) -> ReportBuilder {
        titleValue = value.trimmingCharacters(in: .whitespacesAndNewlines); return self
    }
    @discardableResult func section(_ value: String) -> ReportBuilder { sections.append(value); return self }
    func build() throws -> Report {
        guard !titleValue.isEmpty else { throw DemoError.invalid("title required") }
        return Report(title: titleValue, sections: sections)
    }
}

let builder = ReportBuilder()
expectError { _ = try builder.build() }
let first = try builder.title("Design").section("Intent").build()
builder.section("Tests")
let second = try builder.build()
check(first.sections == ["Intent"] && second.sections.count == 2)
print("OK builder")
