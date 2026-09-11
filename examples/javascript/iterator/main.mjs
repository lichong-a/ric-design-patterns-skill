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
class Bag {
    #values;
    constructor(values) { this.#values = [...values]; }
    *[Symbol.iterator]() {
        yield* this.#values;
    }
}
const bag = new Bag([1, 2, 3]);
const a = bag[Symbol.iterator](), b = bag[Symbol.iterator]();
check(a.next().value === 1);
check(a.next().value === 2);
check(b.next().value === 1);
check([...bag].join(",") === "1,2,3");
check([...new Bag([])].length === 0);
console.log("OK iterator");
export {};
