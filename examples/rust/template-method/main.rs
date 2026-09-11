trait Importer {
    fn parse(&self, value: &str) -> String;
    fn run(&self, raw: &str) -> String { format!("<{}>", self.parse(raw.trim())) }
}
struct UpperImporter;
impl Importer for UpperImporter { fn parse(&self, value: &str) -> String { value.to_uppercase() } }

fn main() {
    assert_eq!(UpperImporter.run(" hello "), "<HELLO>");
    assert_eq!(UpperImporter.run("   "), "<>");
    println!("OK template-method");
}
