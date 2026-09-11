package main

import (
	"fmt"
)

func check(ok bool) {
	if !ok {
		panic("check failed")
	}
}

type Rule struct {
	accepts func(int) bool
	next    *Rule
}

func (r *Rule) Handle(value int) bool {
	return r.accepts(value) && (r.next == nil || r.next.Handle(value))
}

func main() {
	visits := 0
	chain := &Rule{func(n int) bool { return n > 0 }, &Rule{func(n int) bool { visits++; return n < 10 }, nil}}
	check(!chain.Handle(-1) && visits == 0)
	check(chain.Handle(5) && visits == 1)
	check(!chain.Handle(12) && visits == 2)
	fmt.Println("OK chain-of-responsibility")
}
