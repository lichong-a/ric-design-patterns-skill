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

type Counter struct{ Value int }
type AddCommand struct {
	counter       *Counter
	delta, before int
	phase         string
}

func NewAdd(c *Counter, delta int) *AddCommand {
	return &AddCommand{counter: c, delta: delta, phase: "new"}
}
func (c *AddCommand) Execute() error {
	if c.phase != "new" {
		return errors.New("execute once")
	}
	c.before = c.counter.Value
	c.counter.Value += c.delta
	c.phase = "done"
	return nil
}
func (c *AddCommand) Undo() error {
	if c.phase != "done" {
		return errors.New("nothing to undo")
	}
	c.counter.Value = c.before
	c.phase = "undone"
	return nil
}

func main() {
	counter := &Counter{}
	command := NewAdd(counter, 3)
	check(command.Undo() != nil)
	check(command.Execute() == nil && counter.Value == 3)
	check(command.Execute() != nil)
	check(command.Undo() == nil && counter.Value == 0)
	check(command.Undo() != nil)
	fmt.Println("OK command")
}
