export {};

function check(condition: boolean, message = "contract failed"): void {
  if (!condition) throw new Error(message);
}
function expectThrows(action: () => unknown): void {
  let failed = false;
  try { action(); } catch { failed = true; }
  check(failed, "expected an error");
}

interface Button { draw(): string; }
interface Checkbox { mark(): string; }
class ThemedButton implements Button {
  constructor(private readonly theme: string) {}
  draw(): string { return this.theme + ":button"; }
}
class ThemedCheckbox implements Checkbox {
  constructor(private readonly theme: string) {}
  mark(): string { return this.theme + ":checkbox"; }
}
interface WidgetFactory {
  button(): Button;
  checkbox(): Checkbox;
}
class LightFactory implements WidgetFactory {
  button(): Button { return new ThemedButton("light"); }
  checkbox(): Checkbox { return new ThemedCheckbox("light"); }
}
class DarkFactory implements WidgetFactory {
  button(): Button { return new ThemedButton("dark"); }
  checkbox(): Checkbox { return new ThemedCheckbox("dark"); }
}
function screen(factory: WidgetFactory): string {
  return factory.button().draw() + "," + factory.checkbox().mark();
}

check(screen(new LightFactory()) === "light:button,light:checkbox");
check(screen(new DarkFactory()) === "dark:button,dark:checkbox");
console.log("OK abstract-factory");
