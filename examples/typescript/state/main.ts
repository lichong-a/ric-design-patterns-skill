export {};

function check(condition: boolean, message = "contract failed"): void {
  if (!condition) throw new Error(message);
}
function expectThrows(action: () => unknown): void {
  let failed = false;
  try { action(); } catch { failed = true; }
  check(failed, "expected an error");
}

interface GateState {
  readonly name: string;
  coin(): GateState;
  enter(): GateState;
}
class Locked implements GateState {
  readonly name = "locked";
  coin(): GateState { return new Unlocked(); }
  enter(): GateState { return this; }
}
class Unlocked implements GateState {
  readonly name = "unlocked";
  coin(): GateState { return this; }
  enter(): GateState { return new Locked(); }
}
class Gate {
  state: GateState = new Locked();
  coin(): void { this.state = this.state.coin(); }
  enter(): void { this.state = this.state.enter(); }
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
