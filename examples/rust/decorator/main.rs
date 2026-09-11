trait Text { fn render(&self) -> String; }
struct PlainText;
impl Text for PlainText { fn render(&self) -> String { "hi".into() } }
struct PrefixText { inner: Box<dyn Text> }
impl Text for PrefixText { fn render(&self) -> String { format!("!{}", self.inner.render()) } }
struct BracketText { inner: Box<dyn Text> }
impl Text for BracketText { fn render(&self) -> String { format!("[{}]", self.inner.render()) } }

fn main() {
    let a = BracketText { inner: Box::new(PrefixText { inner: Box::new(PlainText) }) };
    let b = PrefixText { inner: Box::new(BracketText { inner: Box::new(PlainText) }) };
    assert_eq!(a.render(), "[!hi]");
    assert_eq!(b.render(), "![hi]");
    println!("OK decorator");
}
