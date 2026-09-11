export {};

function check(condition: boolean, message = "contract failed"): void {
  if (!condition) throw new Error(message);
}
function expectThrows(action: () => unknown): void {
  let failed = false;
  try { action(); } catch { failed = true; }
  check(failed, "expected an error");
}

class Bag implements Iterable<number> {
  readonly #values: readonly number[];
  constructor(values: readonly number[]) { this.#values = [...values]; }
  *[Symbol.iterator](): IterableIterator<number> {
    yield* this.#values;
  }
}

const bag = new Bag([1, 2, 3]);
const a = bag[Symbol.iterator](), b = bag[Symbol.iterator]();
check(a.next().value === 1);
check(a.next().value === 2);
check(b.next().value === 1);
check([...bag].join(",") === "1,2,3");
check([...new Bag([])].length === 0);
console.log("OK iterator");
