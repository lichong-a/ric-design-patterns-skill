use std::collections::HashMap;
use std::rc::Rc;

struct Style { font: String }
#[derive(Default)]
struct StylePool { cache: HashMap<String, Rc<Style>> }
impl StylePool {
    fn get(&mut self, font: &str) -> Rc<Style> {
        Rc::clone(self.cache.entry(font.to_owned()).or_insert_with(|| Rc::new(Style { font: font.to_owned() })))
    }
}
struct Glyph { character: char, x: i32, style: Rc<Style> }

fn main() {
    let mut pool = StylePool::default();
    let a = Glyph { character: 'a', x: 1, style: pool.get("mono") };
    let b = Glyph { character: 'b', x: 8, style: pool.get("mono") };
    assert!(Rc::ptr_eq(&a.style, &b.style));
    assert_ne!(a.x, b.x); assert_ne!(a.character, b.character);
    assert_eq!(a.style.font, "mono");
    assert!(!Rc::ptr_eq(&a.style, &pool.get("serif")));
    println!("OK flyweight");
}
