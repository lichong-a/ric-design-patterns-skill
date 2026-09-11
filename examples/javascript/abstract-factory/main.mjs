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
class ThemedButton {
    theme;
    constructor(theme) {
        this.theme = theme;
    }
    draw() { return this.theme + ":button"; }
}
class ThemedCheckbox {
    theme;
    constructor(theme) {
        this.theme = theme;
    }
    mark() { return this.theme + ":checkbox"; }
}
class LightFactory {
    button() { return new ThemedButton("light"); }
    checkbox() { return new ThemedCheckbox("light"); }
}
class DarkFactory {
    button() { return new ThemedButton("dark"); }
    checkbox() { return new ThemedCheckbox("dark"); }
}
function screen(factory) {
    return factory.button().draw() + "," + factory.checkbox().mark();
}
check(screen(new LightFactory()) === "light:button,light:checkbox");
check(screen(new DarkFactory()) === "dark:button,dark:checkbox");
console.log("OK abstract-factory");
export {};
