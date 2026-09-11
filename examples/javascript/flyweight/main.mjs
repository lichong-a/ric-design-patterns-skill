function check(condition, message = "contract failed") {
    if (!condition)
        throw new Error(message);
}
function expectThrows(action) {
    let failed = false;
    try {
        action();
    }
    catch {
        failed = true;
    }
    check(failed, "expected an error");
}
class Style {
    font;
    constructor(font) {
        this.font = font;
        Object.freeze(this);
    }
}
class StylePool {
    #styles = new Map();
    get(font) {
        let style = this.#styles.get(font);
        if (!style) {
            style = new Style(font);
            this.#styles.set(font, style);
        }
        return style;
    }
}
class Glyph {
    character;
    x;
    style;
    constructor(character, x, style) {
        this.character = character;
        this.x = x;
        this.style = style;
    }
}
const pool = new StylePool();
const a = new Glyph("a", 0, pool.get("mono"));
const b = new Glyph("b", 10, pool.get("mono"));
check(a.style === b.style);
check(a.x !== b.x);
check(pool.get("serif") !== a.style);
console.log("OK flyweight");
export {};
