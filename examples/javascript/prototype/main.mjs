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
class Document {
    paragraphs;
    constructor(paragraphs) {
        this.paragraphs = paragraphs;
    }
    clone() {
        // This schema has two mutable array levels; strings are immutable.
        return new Document(this.paragraphs.map(row => [...row]));
    }
}
const original = new Document([["draft"]]);
const copy = original.clone();
copy.paragraphs[0].push("edited");
check(original.paragraphs[0].length === 1);
check(copy.paragraphs[0].length === 2);
check(copy !== original);
console.log("OK prototype");
export {};
