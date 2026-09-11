export {};

function check(condition: boolean, message = "contract failed"): void {
  if (!condition) throw new Error(message);
}
function expectThrows(action: () => unknown): void {
  let failed = false;
  try { action(); } catch { failed = true; }
  check(failed, "expected an error");
}

interface Text { read(): string; }
class PlainText implements Text {
  constructor(private readonly value: string) {}
  read(): string { return this.value; }
}
class PrefixText implements Text {
  constructor(private readonly inner: Text) {}
  read(): string { return "!" + this.inner.read(); }
}
class BracketText implements Text {
  constructor(private readonly inner: Text) {}
  read(): string { return "[" + this.inner.read() + "]"; }
}

check(new BracketText(new PrefixText(new PlainText("hi"))).read() === "[!hi]");
check(new PrefixText(new BracketText(new PlainText("hi"))).read() === "![hi]");
console.log("OK decorator");
