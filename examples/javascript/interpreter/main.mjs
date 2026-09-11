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
class Literal {
    value;
    constructor(value) {
        this.value = value;
    }
    evaluate(_context) { return this.value; }
}
class Variable {
    name;
    constructor(name) {
        this.name = name;
    }
    evaluate(context) {
        const value = context.get(this.name);
        if (value === undefined)
            throw new Error("missing variable: " + this.name);
        return value;
    }
}
class Add {
    left;
    right;
    constructor(left, right) {
        this.left = left;
        this.right = right;
    }
    evaluate(context) {
        return this.left.evaluate(context) + this.right.evaluate(context);
    }
}
const expr = new Add(new Variable("x"), new Literal(2));
check(expr.evaluate(new Map([["x", 3]])) === 5);
expectThrows(() => expr.evaluate(new Map()));
console.log("OK interpreter");
export {};
