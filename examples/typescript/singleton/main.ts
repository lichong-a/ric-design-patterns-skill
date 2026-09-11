export {};

function check(condition: boolean, message = "contract failed"): void {
  if (!condition) throw new Error(message);
}
function expectThrows(action: () => unknown): void {
  let failed = false;
  try { action(); } catch { failed = true; }
  check(failed, "expected an error");
}

class Settings {
  static readonly #instance = new Settings();
  readonly mode = "production";
  private constructor() { Object.freeze(this); }
  static instance(): Settings { return Settings.#instance; }
}

check(Settings.instance() === Settings.instance());
check(Settings.instance().mode === "production");
console.log("OK singleton");
