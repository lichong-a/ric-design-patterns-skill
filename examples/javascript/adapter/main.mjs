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
class LegacyMeter {
    centimeters() { return 250; }
}
class MeterAdapter {
    legacy;
    constructor(legacy) {
        this.legacy = legacy;
    }
    meters() { return this.legacy.centimeters() / 100; }
}
const length = new MeterAdapter(new LegacyMeter());
check(length.meters() === 2.5);
console.log("OK adapter");
export {};
