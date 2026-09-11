export {};

function check(condition: boolean, message = "contract failed"): void {
  if (!condition) throw new Error(message);
}
function expectThrows(action: () => unknown): void {
  let failed = false;
  try { action(); } catch { failed = true; }
  check(failed, "expected an error");
}

interface Image { render(): string; }
class RealImage implements Image {
  render(): string { return "pixels"; }
}
class ImageProxy implements Image {
  #real?: RealImage;
  loads = 0;
  render(): string {
    if (!this.#real) { this.#real = new RealImage(); this.loads += 1; }
    return this.#real.render();
  }
}

const proxy = new ImageProxy();
check(proxy.loads === 0);
check(proxy.render() === "pixels");
check(proxy.render() === "pixels");
check(proxy.loads === 1);
console.log("OK proxy");
