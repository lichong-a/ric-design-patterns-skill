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
class Snapshot {
    #owner;
    #text;
    constructor(owner, text) { this.#owner = owner; this.#text = text; }
    readFor(owner) {
        if (owner !== this.#owner)
            throw new Error("foreign snapshot");
        return this.#text;
    }
}
class Editor {
    #owner = {};
    #text;
    constructor(text) { this.#text = text; }
    get text() { return this.#text; }
    write(text) { this.#text = text; }
    save() { return new Snapshot(this.#owner, this.#text); }
    restore(snapshot) { this.#text = snapshot.readFor(this.#owner); }
}
const editor = new Editor("draft");
const history = editor.save();
editor.write("edited");
editor.restore(history);
check(editor.text === "draft");
expectThrows(() => new Editor("other").restore(history));
console.log("OK memento");
export {};
