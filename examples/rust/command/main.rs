struct Counter { value: i32 }
struct AddCommand<'a> { counter: &'a mut Counter, delta: i32, before: i32, phase: Phase }
#[derive(PartialEq)]
enum Phase { New, Done, Undone }
impl<'a> AddCommand<'a> {
    fn new(counter: &'a mut Counter, delta: i32) -> Self { Self { counter, delta, before: 0, phase: Phase::New } }
    fn value(&self) -> i32 { self.counter.value }
    fn execute(&mut self) -> Result<(), &'static str> {
        if self.phase != Phase::New { return Err("execute once"); }
        let next = self.counter.value.checked_add(self.delta).ok_or("overflow")?;
        self.before = self.counter.value; self.counter.value = next; self.phase = Phase::Done; Ok(())
    }
    fn undo(&mut self) -> Result<(), &'static str> {
        if self.phase != Phase::Done { return Err("nothing to undo"); }
        self.counter.value = self.before; self.phase = Phase::Undone; Ok(())
    }
}

fn main() {
    let mut counter = Counter { value: 0 };
    {
        let mut command = AddCommand::new(&mut counter, 3);
        assert!(command.undo().is_err());
        assert!(command.execute().is_ok()); assert_eq!(command.value(), 3);
        assert!(command.execute().is_err());
        assert!(command.undo().is_ok()); assert_eq!(command.value(), 0);
        assert!(command.undo().is_err());
    }
    assert_eq!(counter.value, 0);
    println!("OK command");
}
