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
class Locked {
    name = "locked";
    coin() { return new Unlocked(); }
    enter() { return this; }
}
class Unlocked {
    name = "unlocked";
    coin() { return this; }
    enter() { return new Locked(); }
}
class Gate {
    state = new Locked();
    coin() { this.state = this.state.coin(); }
    enter() { this.state = this.state.enter(); }
}
const gate = new Gate();
check(gate.state.name === "locked");
gate.enter();
check(gate.state.name === "locked");
gate.coin();
check(gate.state.name === "unlocked");
gate.enter();
check(gate.state.name === "locked");
console.log("OK state");
export {};
