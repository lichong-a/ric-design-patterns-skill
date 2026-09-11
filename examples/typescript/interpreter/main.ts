export {};

function check(condition: boolean, message = "contract failed"): void {
  if (!condition) throw new Error(message);
}
function expectThrows(action: () => unknown): void {
  let failed = false;
  try { action(); } catch { failed = true; }
  check(failed, "expected an error");
}

type Context = ReadonlyMap<string, number>;
interface Expr { evaluate(context: Context): number; }
class Literal implements Expr {
  constructor(private readonly value: number) {}
  evaluate(_context: Context): number { return this.value; }
}
class Variable implements Expr {
  constructor(private readonly name: string) {}
  evaluate(context: Context): number {
    const value = context.get(this.name);
    if (value === undefined) throw new Error("missing variable: " + this.name);
    return value;
  }
}
class Add implements Expr {
  constructor(private readonly left: Expr, private readonly right: Expr) {}
  evaluate(context: Context): number {
    return this.left.evaluate(context) + this.right.evaluate(context);
  }
}

const expr = new Add(new Variable("x"), new Literal(2));
check(expr.evaluate(new Map([["x", 3]])) === 5);
expectThrows(() => expr.evaluate(new Map()));
console.log("OK interpreter");
