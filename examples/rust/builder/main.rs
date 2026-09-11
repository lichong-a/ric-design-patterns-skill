#[derive(Debug)]
struct Report { title: String, sections: Vec<String> }
#[derive(Default)]
struct ReportBuilder { title: String, sections: Vec<String> }
impl ReportBuilder {
    fn title(&mut self, value: &str) -> &mut Self { self.title = value.trim().to_owned(); self }
    fn section(&mut self, value: &str) -> &mut Self { self.sections.push(value.to_owned()); self }
    fn build(&self) -> Result<Report, &'static str> {
        if self.title.is_empty() { return Err("title required"); }
        Ok(Report { title: self.title.clone(), sections: self.sections.clone() })
    }
}

fn main() {
    let mut builder = ReportBuilder::default();
    assert!(builder.build().is_err());
    let first = builder.title("Design").section("Intent").build().expect("valid report");
    builder.section("Tests");
    let second = builder.build().expect("valid report");
    assert_eq!(first.title, "Design");
    assert_eq!(first.sections, vec!["Intent".to_owned()]);
    assert_eq!(second.sections.len(), 2);
    println!("OK builder");
}
