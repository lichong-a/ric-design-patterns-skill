trait Renderer { fn render(&self) -> &'static str; }
struct PlainRenderer;
impl Renderer for PlainRenderer { fn render(&self) -> &'static str { "plain" } }
struct JsonRenderer;
impl Renderer for JsonRenderer { fn render(&self) -> &'static str { "json" } }
trait Publisher {
    fn make(&self) -> Box<dyn Renderer>;
    fn publish(&self) -> String { format!("published:{}", self.make().render()) }
}
struct PlainPublisher;
impl Publisher for PlainPublisher { fn make(&self) -> Box<dyn Renderer> { Box::new(PlainRenderer) } }
struct JsonPublisher;
impl Publisher for JsonPublisher { fn make(&self) -> Box<dyn Renderer> { Box::new(JsonRenderer) } }

fn main() {
    assert_eq!(PlainPublisher.publish(), "published:plain");
    assert_eq!(JsonPublisher.publish(), "published:json");
    println!("OK factory-method");
}
