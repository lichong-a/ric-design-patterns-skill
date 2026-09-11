export {};

function check(condition: boolean, message = "contract failed"): void {
  if (!condition) throw new Error(message);
}
function expectThrows(action: () => unknown): void {
  let failed = false;
  try { action(); } catch { failed = true; }
  check(failed, "expected an error");
}

class Toggle {
  constructor(private readonly changed: (selected: boolean) => void) {}
  select(value: boolean): void { this.changed(value); }
}
class SubmitButton { enabled = false; }
class Dialog {
  readonly button = new SubmitButton();
  readonly toggle = new Toggle(selected => this.changed(selected));
  private changed(selected: boolean): void { this.button.enabled = selected; }
}

const dialog = new Dialog();
check(!dialog.button.enabled);
dialog.toggle.select(true);
check(dialog.button.enabled);
dialog.toggle.select(false);
check(!dialog.button.enabled);
console.log("OK mediator");
