package main

import (
	"errors"
	"fmt"
)

func check(ok bool) {
	if !ok {
		panic("check failed")
	}
}

type Pricing struct{ Rule func(int) int }

func (p Pricing) Quote(base int) (int, error) {
	if base < 0 {
		return 0, errors.New("base must be nonnegative")
	}
	return p.Rule(base), nil
}
func Discount(amount int) func(int) int {
	return func(base int) int {
		if base < amount {
			return 0
		}
		return base - amount
	}
}

func main() {
	p := Pricing{Rule: Discount(10)}
	x, err := p.Quote(100)
	check(err == nil && x == 90)
	p.Rule = Discount(20)
	x, err = p.Quote(100)
	check(err == nil && x == 80)
	x, err = p.Quote(5)
	check(err == nil && x == 0)
	_, err = p.Quote(-1)
	check(err != nil)
	fmt.Println("OK strategy")
}
