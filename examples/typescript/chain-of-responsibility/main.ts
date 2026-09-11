export {};

function check(condition: boolean, message = "contract failed"): void {
  if (!condition) throw new Error(message);
}
function expectThrows(action: () => unknown): void {
  let failed = false;
  try { action(); } catch { failed = true; }
  check(failed, "expected an error");
}

class Rule {
  constructor(private readonly predicate: (value: number) => boolean, private readonly next?: Rule) {}
  handle(value: number): boolean {
    if (!this.predicate(value)) return false;
    return this.next ? this.next.handle(value) : true;
  }
}

const visits: number[] = [];
const chain = new Rule(n => n > 0, new Rule(n => { visits.push(n); return n < 1000; }));
check(chain.handle(100));
check(!chain.handle(-1));
check(visits.length === 1 && visits[0] === 100);
check(!chain.handle(1000));
console.log("OK chain-of-responsibility");
