export {};

function check(condition: boolean, message = "contract failed"): void {
  if (!condition) throw new Error(message);
}
function expectThrows(action: () => unknown): void {
  let failed = false;
  try { action(); } catch { failed = true; }
  check(failed, "expected an error");
}

class Inventory {
  reserve(quantity: number): string {
    if (!Number.isInteger(quantity) || quantity <= 0) throw new Error("invalid quantity");
    return `reserved:${quantity}`;
  }
}
class Receipts {
  create(reservation: string): string { return "receipt:" + reservation; }
}
class Checkout {
  constructor(private readonly inventory: Inventory, private readonly receipts: Receipts) {}
  place(quantity: number): string {
    return this.receipts.create(this.inventory.reserve(quantity));
  }
}

const checkout = new Checkout(new Inventory(), new Receipts());
check(checkout.place(2) === "receipt:reserved:2");
expectThrows(() => checkout.place(0));
expectThrows(() => checkout.place(Number.NaN));
console.log("OK facade");
