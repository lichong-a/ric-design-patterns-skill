package patterns.adapter

fun expectError(action: () -> Unit) {
    var failed = false
    try { action() } catch (_: RuntimeException) { failed = true }
    check(failed)
}

class LegacySensor { fun centimeters() = 250 }
interface MeterReader { fun meters(): Double }
class SensorAdapter(private val sensor: LegacySensor) : MeterReader {
    override fun meters() = sensor.centimeters() / 100.0
}

fun main() {
    val reader: MeterReader = SensorAdapter(LegacySensor())
    check(reader.meters() == 2.5)
    println("OK adapter")
}
