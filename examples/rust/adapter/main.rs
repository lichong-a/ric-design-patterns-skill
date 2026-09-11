struct LegacySensor;
impl LegacySensor { fn centimeters(&self) -> u32 { 250 } }
trait MeterReader { fn meters(&self) -> f64; }
struct SensorAdapter { sensor: LegacySensor }
impl MeterReader for SensorAdapter { fn meters(&self) -> f64 { f64::from(self.sensor.centimeters()) / 100.0 } }

fn main() {
    let reader: Box<dyn MeterReader> = Box::new(SensorAdapter { sensor: LegacySensor });
    assert_eq!(reader.meters(), 2.5);
    println!("OK adapter");
}
