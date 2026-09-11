export {};

function check(condition: boolean, message = "contract failed"): void {
  if (!condition) throw new Error(message);
}
function expectThrows(action: () => unknown): void {
  let failed = false;
  try { action(); } catch { failed = true; }
  check(failed, "expected an error");
}

class Counter { value = 0; }
class AddCommand {
  #before = 0;
  #phase: "new" | "done" | "undone" = "new";
  constructor(private readonly counter: Counter, private readonly amount: number) {}
  execute(): void {
    if (this.#phase !== "new") throw new Error("already executed");
    this.#before = this.counter.value;
    this.counter.value += this.amount;
    this.#phase = "done";
  }
  undo(): void {
    if (this.#phase !== "done") throw new Error("nothing to undo");
    this.counter.value = this.#before;
    this.#phase = "undone";
  }
}

const counter = new Counter();
const command = new AddCommand(counter, 5);
command.execute();
check(counter.value === 5);
expectThrows(() => command.execute());
command.undo();
check(counter.value === 0);
expectThrows(() => command.undo());
console.log("OK command");
