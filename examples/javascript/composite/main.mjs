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
class LineItem {
    value;
    constructor(value) {
        this.value = value;
    }
    total() { return this.value; }
}
class Bundle {
    #children;
    constructor(children) { this.#children = [...children]; }
    total() {
        return this.#children.reduce((sum, child) => sum + child.total(), 0);
    }
}
const root = new Bundle([new LineItem(10), new Bundle([new LineItem(20), new LineItem(30)])]);
check(root.total() === 60);
check(new Bundle([]).total() === 0);
console.log("OK composite");
export {};
