package main

import (
	"fmt"
)

func check(ok bool) {
	if !ok {
		panic("check failed")
	}
}

type Events struct {
	sequence  int
	listeners map[int]func(int)
}

func NewEvents() *Events { return &Events{listeners: make(map[int]func(int))} }
func (e *Events) Subscribe(fn func(int)) int {
	e.sequence++
	e.listeners[e.sequence] = fn
	return e.sequence
}
func (e *Events) Unsubscribe(id int) { delete(e.listeners, id) }
func (e *Events) Emit(value int) {
	snapshot := make([]func(int), 0, len(e.listeners))
	for _, fn := range e.listeners {
		snapshot = append(snapshot, fn)
	}
	for _, fn := range snapshot {
		fn(value)
	}
}

func main() {
	events := NewEvents()
	seen := []int{}
	id := events.Subscribe(func(n int) { seen = append(seen, n) })
	events.Emit(1)
	events.Unsubscribe(id)
	events.Emit(2)
	check(len(seen) == 1 && seen[0] == 1)
	self := 0
	self = events.Subscribe(func(int) { events.Unsubscribe(self) })
	events.Emit(3)
	events.Emit(4)
	fmt.Println("OK observer")
}
