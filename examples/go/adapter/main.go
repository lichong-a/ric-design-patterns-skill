package main

import (
	"fmt"
)

func check(ok bool) {
	if !ok {
		panic("check failed")
	}
}

type LegacySensor struct{}

func (LegacySensor) Centimeters() int { return 250 }

type MeterReader interface{ Meters() float64 }
type SensorAdapter struct{ sensor LegacySensor }

func (a SensorAdapter) Meters() float64 { return float64(a.sensor.Centimeters()) / 100 }

func main() {
	var reader MeterReader = SensorAdapter{sensor: LegacySensor{}}
	check(reader.Meters() == 2.5)
	fmt.Println("OK adapter")
}
