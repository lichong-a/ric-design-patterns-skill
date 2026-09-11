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
class Settings {
    static #instance = new Settings();
    mode = "production";
    constructor() { Object.freeze(this); }
    static instance() { return Settings.#instance; }
}
check(Settings.instance() === Settings.instance());
check(Settings.instance().mode === "production");
console.log("OK singleton");
export {};
