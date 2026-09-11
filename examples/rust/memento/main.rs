use std::rc::Rc;

struct Snapshot { owner: Rc<u8>, text: String }
struct Editor { owner: Rc<u8>, text: String }
impl Editor {
    fn new() -> Self { Self { owner: Rc::new(0), text: String::new() } }
    fn save(&self) -> Snapshot { Snapshot { owner: Rc::clone(&self.owner), text: self.text.clone() } }
    fn restore(&mut self, snapshot: &Snapshot) -> Result<(), &'static str> {
        if !Rc::ptr_eq(&self.owner, &snapshot.owner) { return Err("foreign snapshot"); }
        self.text = snapshot.text.clone(); Ok(())
    }
}

fn main() {
    let mut a = Editor::new(); let mut b = Editor::new();
    a.text = "one".into(); let saved = a.save(); a.text = "two".into();
    assert!(a.restore(&saved).is_ok()); assert_eq!(a.text, "one");
    assert!(b.restore(&saved).is_err());
    println!("OK memento");
}
