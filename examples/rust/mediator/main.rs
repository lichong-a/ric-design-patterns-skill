enum UiEvent { Toggled(bool) }
#[derive(Default)]
struct Toggle { checked: bool }
impl Toggle {
    fn set(&mut self, value: bool) -> UiEvent { self.checked = value; UiEvent::Toggled(value) }
}
#[derive(Default)]
struct SubmitButton { enabled: bool }
#[derive(Default)]
struct Dialog { toggle: Toggle, submit: SubmitButton }
impl Dialog {
    fn set_checked(&mut self, value: bool) {
        let event = self.toggle.set(value);
        self.handle(event);
    }
    fn handle(&mut self, event: UiEvent) {
        match event { UiEvent::Toggled(value) => self.submit.enabled = value }
    }
}

fn main() {
    let mut dialog = Dialog::default(); assert!(!dialog.submit.enabled);
    dialog.set_checked(true); assert!(dialog.submit.enabled && dialog.toggle.checked);
    dialog.set_checked(false); assert!(!dialog.submit.enabled);
    println!("OK mediator");
}
