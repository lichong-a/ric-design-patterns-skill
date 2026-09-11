package main

import (
	"fmt"
)

func check(ok bool) {
	if !ok {
		panic("check failed")
	}
}

type Image interface{ Read() string }
type RealImage struct{}

func (*RealImage) Read() string { return "pixels" }

type LazyImage struct {
	real  *RealImage
	loads int
}

func (p *LazyImage) Read() string {
	if p.real == nil {
		p.real = &RealImage{}
		p.loads++
	}
	return p.real.Read()
}

func main() {
	p := &LazyImage{}
	var image Image = p
	check(p.loads == 0)
	check(image.Read() == "pixels" && image.Read() == "pixels")
	check(p.loads == 1)
	fmt.Println("OK proxy")
}
