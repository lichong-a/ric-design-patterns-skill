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
class Events {
    #listeners = new Map();
    #next = 0;
    subscribe(listener) {
        this.#next += 1;
        this.#listeners.set(this.#next, listener);
        return this.#next;
    }
    unsubscribe(token) { this.#listeners.delete(token); }
    emit(value) {
        for (const listener of [...this.#listeners.values()])
            listener(value);
    }
}
const events = new Events();
const seen = [];
const token = events.subscribe(value => seen.push(value));
events.emit(3);
events.unsubscribe(token);
events.emit(9);
check(seen.join(",") === "3");
const late = [];
const other = events.subscribe(value => late.push(value));
events.subscribe(() => events.unsubscribe(other));
events.emit(1);
events.emit(2);
check(late.join(",") === "1");
console.log("OK observer");
export {};
