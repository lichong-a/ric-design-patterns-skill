export {};

function check(condition: boolean, message = "contract failed"): void {
  if (!condition) throw new Error(message);
}
function expectThrows(action: () => unknown): void {
  let failed = false;
  try { action(); } catch { failed = true; }
  check(failed, "expected an error");
}

interface Item { total(): number; }
class LineItem implements Item {
  constructor(private readonly value: number) {}
  total(): number { return this.value; }
}
class Bundle implements Item {
  readonly #children: readonly Item[];
  constructor(children: readonly Item[]) { this.#children = [...children]; }
  total(): number {
    return this.#children.reduce((sum, child) => sum + child.total(), 0);
  }
}

const root = new Bundle([new LineItem(10), new Bundle([new LineItem(20), new LineItem(30)])]);
check(root.total() === 60);
check(new Bundle([]).total() === 0);
console.log("OK composite");
