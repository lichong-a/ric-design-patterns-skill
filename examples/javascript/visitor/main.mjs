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
class TextNode {
    value;
    constructor(value) {
        this.value = value;
    }
    accept(visitor) { return visitor.visitText(this); }
}
class NumberNode {
    value;
    constructor(value) {
        this.value = value;
    }
    accept(visitor) { return visitor.visitNumber(this); }
}
class RenderVisitor {
    visitText(node) { return "text:" + node.value; }
    visitNumber(node) { return `number:${node.value}`; }
}
const visitor = new RenderVisitor();
const nodes = [new TextNode("a"), new NumberNode(7)];
check(nodes.map(node => node.accept(visitor)).join(",") === "text:a,number:7");
console.log("OK visitor");
export {};
