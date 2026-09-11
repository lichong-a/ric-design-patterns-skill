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
class PlainText {
    value;
    constructor(value) {
        this.value = value;
    }
    read() { return this.value; }
}
class PrefixText {
    inner;
    constructor(inner) {
        this.inner = inner;
    }
    read() { return "!" + this.inner.read(); }
}
class BracketText {
    inner;
    constructor(inner) {
        this.inner = inner;
    }
    read() { return "[" + this.inner.read() + "]"; }
}
check(new BracketText(new PrefixText(new PlainText("hi"))).read() === "[!hi]");
check(new PrefixText(new BracketText(new PlainText("hi"))).read() === "![hi]");
console.log("OK decorator");
export {};
