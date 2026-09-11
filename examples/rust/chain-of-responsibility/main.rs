use std::rc::Rc;
use std::cell::Cell;

struct Rule { accepts: Box<dyn Fn(i32) -> bool>, next: Option<Box<Rule>> }
impl Rule {
    fn handle(&self, value: i32) -> bool {
        (self.accepts)(value) && self.next.as_ref().map_or(true, |next| next.handle(value))
    }
}

fn main() {
    let visits = Rc::new(Cell::new(0)); let counter = Rc::clone(&visits);
    let chain = Rule {
        accepts: Box::new(|n| n > 0),
        next: Some(Box::new(Rule { accepts: Box::new(move |n| { counter.set(counter.get() + 1); n < 10 }), next: None })),
    };
    assert!(!chain.handle(-1)); assert_eq!(visits.get(), 0);
    assert!(chain.handle(5)); assert_eq!(visits.get(), 1);
    assert!(!chain.handle(12)); assert_eq!(visits.get(), 2);
    println!("OK chain-of-responsibility");
}
