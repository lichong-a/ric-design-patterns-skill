export {};

function check(condition: boolean, message = "contract failed"): void {
  if (!condition) throw new Error(message);
}
function expectThrows(action: () => unknown): void {
  let failed = false;
  try { action(); } catch { failed = true; }
  check(failed, "expected an error");
}

class Style {
  constructor(readonly font: string) { Object.freeze(this); }
}
class StylePool {
  #styles = new Map<string, Style>();
  get(font: string): Style {
    let style = this.#styles.get(font);
    if (!style) { style = new Style(font); this.#styles.set(font, style); }
    return style;
  }
}
class Glyph {
  constructor(readonly character: string, readonly x: number, readonly style: Style) {}
}

const pool = new StylePool();
const a = new Glyph("a", 0, pool.get("mono"));
const b = new Glyph("b", 10, pool.get("mono"));
check(a.style === b.style);
check(a.x !== b.x);
check(pool.get("serif") !== a.style);
console.log("OK flyweight");
