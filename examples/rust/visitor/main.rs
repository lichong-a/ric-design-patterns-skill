trait NodeVisitor { fn visit_text(&self, node: &TextNode) -> String; fn visit_number(&self, node: &NumberNode) -> String; }
trait Node { fn accept(&self, visitor: &dyn NodeVisitor) -> String; }
struct TextNode { value: String }
impl Node for TextNode { fn accept(&self, visitor: &dyn NodeVisitor) -> String { visitor.visit_text(self) } }
struct NumberNode { value: i32 }
impl Node for NumberNode { fn accept(&self, visitor: &dyn NodeVisitor) -> String { visitor.visit_number(self) } }
struct RenderVisitor;
impl NodeVisitor for RenderVisitor {
    fn visit_text(&self, node: &TextNode) -> String { format!("text:{}", node.value) }
    fn visit_number(&self, node: &NumberNode) -> String { format!("number:{}", node.value) }
}

fn main() {
    let visitor = RenderVisitor;
    assert_eq!(TextNode { value: "a".into() }.accept(&visitor), "text:a");
    assert_eq!(NumberNode { value: 7 }.accept(&visitor), "number:7");
    println!("OK visitor");
}
