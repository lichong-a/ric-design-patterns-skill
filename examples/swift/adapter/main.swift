import Foundation

func check(_ condition: @autoclosure () -> Bool) {
    precondition(condition(), "check failed")
}
enum DemoError: Error { case invalid(String) }
func expectError(_ action: () throws -> Void) {
    var failed = false
    do { try action() } catch { failed = true }
    check(failed)
}

struct LegacySensor { func centimeters() -> Int { 250 } }
protocol MeterReader { func meters() -> Double }
struct SensorAdapter: MeterReader {
    let sensor: LegacySensor
    func meters() -> Double { Double(sensor.centimeters()) / 100.0 }
}

let reader: any MeterReader = SensorAdapter(sensor: LegacySensor())
check(reader.meters() == 2.5)
print("OK adapter")
