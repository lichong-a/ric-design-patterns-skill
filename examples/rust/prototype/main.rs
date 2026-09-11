#[derive(Clone)]
struct Document { title: String, paragraphs: Vec<Vec<String>> }

fn main() {
    let original = Document { title: "Design".into(), paragraphs: vec![vec!["one".into()]] };
    let mut copied = original.clone();
    copied.paragraphs[0][0] = "changed".into();
    copied.paragraphs[0].push("two".into());
    assert_eq!(original.title, "Design");
    assert_eq!(original.paragraphs, vec![vec!["one".to_owned()]]);
    assert_eq!(copied.paragraphs[0].len(), 2);
    println!("OK prototype");
}
