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

protocol NodeVisitor { func visitText(_ node: TextNode) -> String; func visitNumber(_ node: NumberNode) -> String }
protocol Node { func accept(_ visitor: any NodeVisitor) -> String }
struct TextNode: Node {
    let value: String
    func accept(_ visitor: any NodeVisitor) -> String { visitor.visitText(self) }
}
struct NumberNode: Node {
    let value: Int
    func accept(_ visitor: any NodeVisitor) -> String { visitor.visitNumber(self) }
}
struct RenderVisitor: NodeVisitor {
    func visitText(_ node: TextNode) -> String { "text:" + node.value }
    func visitNumber(_ node: NumberNode) -> String { "number:\(node.value)" }
}

let visitor = RenderVisitor()
check(TextNode(value: "a").accept(visitor) == "text:a")
check(NumberNode(value: 7).accept(visitor) == "number:7")
print("OK visitor")
