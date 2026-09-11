export {};

function check(condition: boolean, message = "contract failed"): void {
  if (!condition) throw new Error(message);
}
function expectThrows(action: () => unknown): void {
  let failed = false;
  try { action(); } catch { failed = true; }
  check(failed, "expected an error");
}

class Document {
  constructor(public paragraphs: string[][]) {}
  clone(): Document {
    // This schema has two mutable array levels; strings are immutable.
    return new Document(this.paragraphs.map(row => [...row]));
  }
}

const original = new Document([["draft"]]);
const copy = original.clone();
copy.paragraphs[0].push("edited");
check(original.paragraphs[0].length === 1);
check(copy.paragraphs[0].length === 2);
check(copy !== original);
console.log("OK prototype");
