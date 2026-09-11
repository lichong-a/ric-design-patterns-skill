package main

import (
	"fmt"
)

func check(ok bool) {
	if !ok {
		panic("check failed")
	}
}

type Bag struct{ values []int }

func NewBag(values []int) Bag { return Bag{append([]int(nil), values...)} }

type Cursor struct {
	values []int
	index  int
}

func (b Bag) Iterator() *Cursor { return &Cursor{values: b.values} }
func (c *Cursor) Next() (int, bool) {
	if c.index >= len(c.values) {
		return 0, false
	}
	value := c.values[c.index]
	c.index++
	return value, true
}

func main() {
	bag := NewBag([]int{1, 2, 3})
	a, b := bag.Iterator(), bag.Iterator()
	x, ok := a.Next()
	check(ok && x == 1)
	x, ok = a.Next()
	check(ok && x == 2)
	x, ok = b.Next()
	check(ok && x == 1)
	empty := NewBag(nil).Iterator()
	_, ok = empty.Next()
	check(!ok)
	a.Next()
	_, ok = a.Next()
	check(!ok)
	fmt.Println("OK iterator")
}
