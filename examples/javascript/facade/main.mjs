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
class Inventory {
    reserve(quantity) {
        if (!Number.isInteger(quantity) || quantity <= 0)
            throw new Error("invalid quantity");
        return `reserved:${quantity}`;
    }
}
class Receipts {
    create(reservation) { return "receipt:" + reservation; }
}
class Checkout {
    inventory;
    receipts;
    constructor(inventory, receipts) {
        this.inventory = inventory;
        this.receipts = receipts;
    }
    place(quantity) {
        return this.receipts.create(this.inventory.reserve(quantity));
    }
}
const checkout = new Checkout(new Inventory(), new Receipts());
check(checkout.place(2) === "receipt:reserved:2");
expectThrows(() => checkout.place(0));
expectThrows(() => checkout.place(Number.NaN));
console.log("OK facade");
export {};
