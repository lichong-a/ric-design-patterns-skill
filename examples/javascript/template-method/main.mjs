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
class Importer {
    run(raw) {
        const loaded = raw.trim();
        const parsed = this.parse(loaded);
        return "<" + parsed + ">";
    }
}
class UpperImporter extends Importer {
    parse(text) { return text.toUpperCase(); }
}
check(new UpperImporter().run(" hello ") === "<HELLO>");
console.log("OK template-method");
export {};
