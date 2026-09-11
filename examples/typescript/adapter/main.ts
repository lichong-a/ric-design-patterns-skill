export {};

function check(condition: boolean, message = "contract failed"): void {
  if (!condition) throw new Error(message);
}
function expectThrows(action: () => unknown): void {
  let failed = false;
  try { action(); } catch { failed = true; }
  check(failed, "expected an error");
}

interface Length { meters(): number; }
class LegacyMeter {
  centimeters(): number { return 250; }
}
class MeterAdapter implements Length {
  constructor(private readonly legacy: LegacyMeter) {}
  meters(): number { return this.legacy.centimeters() / 100; }
}

const length: Length = new MeterAdapter(new LegacyMeter());
check(length.meters() === 2.5);
console.log("OK adapter");
