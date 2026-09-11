trait GateState { fn is_open(&self) -> bool; fn coin(&self) -> Box<dyn GateState>; fn enter(&self) -> Box<dyn GateState>; }
struct Locked;
impl GateState for Locked {
    fn is_open(&self) -> bool { false }
    fn coin(&self) -> Box<dyn GateState> { Box::new(Unlocked) }
    fn enter(&self) -> Box<dyn GateState> { Box::new(Locked) }
}
struct Unlocked;
impl GateState for Unlocked {
    fn is_open(&self) -> bool { true }
    fn coin(&self) -> Box<dyn GateState> { Box::new(Unlocked) }
    fn enter(&self) -> Box<dyn GateState> { Box::new(Locked) }
}
struct Gate { state: Box<dyn GateState> }
impl Gate {
    fn new() -> Self { Self { state: Box::new(Locked) } }
    fn coin(&mut self) { self.state = self.state.coin(); }
    fn enter(&mut self) { self.state = self.state.enter(); }
}

fn main() {
    let mut gate = Gate::new(); assert!(!gate.state.is_open());
    gate.enter(); assert!(!gate.state.is_open());
    gate.coin(); assert!(gate.state.is_open());
    gate.coin(); assert!(gate.state.is_open());
    gate.enter(); assert!(!gate.state.is_open());
    println!("OK state");
}
