export {};

function check(condition: boolean, message = "contract failed"): void {
  if (!condition) throw new Error(message);
}
function expectThrows(action: () => unknown): void {
  let failed = false;
  try { action(); } catch { failed = true; }
  check(failed, "expected an error");
}

abstract class Importer {
  run(raw: string): string {
    const loaded = raw.trim();
    const parsed = this.parse(loaded);
    return "<" + parsed + ">";
  }
  protected abstract parse(text: string): string;
}
class UpperImporter extends Importer {
  protected parse(text: string): string { return text.toUpperCase(); }
}

check(new UpperImporter().run(" hello ") === "<HELLO>");
console.log("OK template-method");
