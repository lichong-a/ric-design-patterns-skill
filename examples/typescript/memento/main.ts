export {};

function check(condition: boolean, message = "contract failed"): void {
  if (!condition) throw new Error(message);
}
function expectThrows(action: () => unknown): void {
  let failed = false;
  try { action(); } catch { failed = true; }
  check(failed, "expected an error");
}

class Snapshot {
  readonly #owner: object;
  readonly #text: string;
  constructor(owner: object, text: string) { this.#owner = owner; this.#text = text; }
  readFor(owner: object): string {
    if (owner !== this.#owner) throw new Error("foreign snapshot");
    return this.#text;
  }
}
class Editor {
  readonly #owner = {};
  #text: string;
  constructor(text: string) { this.#text = text; }
  get text(): string { return this.#text; }
  write(text: string): void { this.#text = text; }
  save(): Snapshot { return new Snapshot(this.#owner, this.#text); }
  restore(snapshot: Snapshot): void { this.#text = snapshot.readFor(this.#owner); }
}

const editor = new Editor("draft");
const history = editor.save();
editor.write("edited");
editor.restore(history);
check(editor.text === "draft");
expectThrows(() => new Editor("other").restore(history));
console.log("OK memento");
