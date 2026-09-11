package main

import (
	"fmt"
)

func check(ok bool) {
	if !ok {
		panic("check failed")
	}
}

type Item interface{ Total() int }
type LineItem struct{ price int }

func (i LineItem) Total() int { return i.price }

type Bundle struct{ children []Item }

func (b Bundle) Total() int {
	total := 0
	for _, child := range b.children {
		total += child.Total()
	}
	return total
}

func main() {
	root := Bundle{[]Item{LineItem{10}, Bundle{[]Item{LineItem{20}, LineItem{30}}}}}
	check(root.Total() == 60)
	check((Bundle{}).Total() == 0)
	fmt.Println("OK composite")
}
