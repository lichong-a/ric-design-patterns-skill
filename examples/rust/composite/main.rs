trait Item { fn total(&self) -> i32; }
struct LineItem { price: i32 }
impl Item for LineItem { fn total(&self) -> i32 { self.price } }
struct Bundle { children: Vec<Box<dyn Item>> }
impl Item for Bundle { fn total(&self) -> i32 { self.children.iter().map(|item| item.total()).sum() } }

fn main() {
    let root = Bundle { children: vec![
        Box::new(LineItem { price: 10 }),
        Box::new(Bundle { children: vec![Box::new(LineItem { price: 20 }), Box::new(LineItem { price: 30 })] }),
    ] };
    assert_eq!(root.total(), 60);
    assert_eq!(Bundle { children: vec![] }.total(), 0);
    println!("OK composite");
}
