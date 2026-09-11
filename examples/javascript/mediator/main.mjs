function check(condition, message = "contract failed") {
    if (!condition)
        throw new Error(message);
}
function expectThrows(action) {
    let failed = false;
    try {
        action();
    }
    catch {
        failed = true;
    }
    check(failed, "expected an error");
}
class Toggle {
    changed;
    constructor(changed) {
        this.changed = changed;
    }
    select(value) { this.changed(value); }
}
class SubmitButton {
    enabled = false;
}
class Dialog {
    button = new SubmitButton();
    toggle = new Toggle(selected => this.changed(selected));
    changed(selected) { this.button.enabled = selected; }
}
const dialog = new Dialog();
check(!dialog.button.enabled);
dialog.toggle.select(true);
check(dialog.button.enabled);
dialog.toggle.select(false);
check(!dialog.button.enabled);
console.log("OK mediator");
export {};
