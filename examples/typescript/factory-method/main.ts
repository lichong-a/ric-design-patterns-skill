export {};

function check(condition: boolean, message = "contract failed"): void {
  if (!condition) throw new Error(message);
}
function expectThrows(action: () => unknown): void {
  let failed = false;
  try { action(); } catch { failed = true; }
  check(failed, "expected an error");
}

interface Renderer { render(): string; }
class PlainRenderer implements Renderer {
  render(): string { return "plain"; }
}
class JsonRenderer implements Renderer {
  render(): string { return '{"format":"json"}'; }
}
abstract class Publisher {
  protected abstract make(): Renderer;
  publish(): string { return "published:" + this.make().render(); }
}
class PlainPublisher extends Publisher {
  protected make(): Renderer { return new PlainRenderer(); }
}
class JsonPublisher extends Publisher {
  protected make(): Renderer { return new JsonRenderer(); }
}

check(new PlainPublisher().publish() === "published:plain");
check(new JsonPublisher().publish() === 'published:{"format":"json"}');
console.log("OK factory-method");
