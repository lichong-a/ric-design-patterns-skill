use std::collections::BTreeMap;
use std::rc::Rc;
use std::cell::Cell;
use std::cell::RefCell;

type Listener = Rc<dyn Fn(&mut Events, i32)>;
#[derive(Default)]
struct Events { sequence: usize, listeners: BTreeMap<usize, Listener> }
impl Events {
    fn subscribe(&mut self, listener: impl Fn(&mut Events, i32) + 'static) -> usize {
        self.sequence += 1;
        self.listeners.insert(self.sequence, Rc::new(listener)); self.sequence
    }
    fn unsubscribe(&mut self, token: usize) { self.listeners.remove(&token); }
    fn emit(&mut self, value: i32) {
        let snapshot: Vec<Listener> = self.listeners.values().cloned().collect();
        for listener in snapshot { listener(self, value); }
    }
}

fn main() {
    let mut events = Events::default();
    let seen = Rc::new(RefCell::new(Vec::new())); let sink = Rc::clone(&seen);
    let token = events.subscribe(move |_, n| sink.borrow_mut().push(n));
    events.emit(1); events.unsubscribe(token); events.emit(2);
    assert_eq!(*seen.borrow(), vec![1]);
    let self_token = Rc::new(Cell::new(0)); let id = Rc::clone(&self_token);
    self_token.set(events.subscribe(move |events, _| events.unsubscribe(id.get())));
    events.emit(3); events.emit(4);
    println!("OK observer");
}
