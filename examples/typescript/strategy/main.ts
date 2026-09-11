export {};

function check(condition: boolean, message = "contract failed"): void {
  if (!condition) throw new Error(message);
}
function expectThrows(action: () => unknown): void {
  let failed = false;
  try { action(); } catch { failed = true; }
  check(failed, "expected an error");
}

type Discount = (amount: number) => number;
class Pricing {
  constructor(private readonly discount: Discount) {}
  total(base: number): number {
    if (!Number.isFinite(base) || base < 0) throw new Error("invalid base");
    return this.discount(base);
  }
}

check(new Pricing(amount => Math.max(0, amount - 10)).total(100) === 90);
check(new Pricing(amount => Math.max(0, amount - 20)).total(100) === 80);
check(new Pricing(amount => Math.max(0, amount - 20)).total(5) === 0);
expectThrows(() => new Pricing(amount => amount).total(Number.NaN));
console.log("OK strategy");
