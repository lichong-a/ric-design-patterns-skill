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
class Rule {
    predicate;
    next;
    constructor(predicate, next) {
        this.predicate = predicate;
        this.next = next;
    }
    handle(value) {
        if (!this.predicate(value))
            return false;
        return this.next ? this.next.handle(value) : true;
    }
}
const visits = [];
const chain = new Rule(n => n > 0, new Rule(n => { visits.push(n); return n < 1000; }));
check(chain.handle(100));
check(!chain.handle(-1));
check(visits.length === 1 && visits[0] === 100);
check(!chain.handle(1000));
console.log("OK chain-of-responsibility");
export {};
