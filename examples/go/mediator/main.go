package main

import (
	"fmt"
)

func check(ok bool) {
	if !ok {
		panic("check failed")
	}
}

type Toggle struct{ changed func(bool) }

func (t *Toggle) Set(value bool) {
	if t.changed != nil {
		t.changed(value)
	}
}

type SubmitButton struct{ Enabled bool }
type Dialog struct {
	Toggle Toggle
	Submit SubmitButton
}

func NewDialog() *Dialog {
	d := &Dialog{}
	d.Toggle.changed = func(value bool) { d.Submit.Enabled = value }
	return d
}

func main() {
	d := NewDialog()
	check(!d.Submit.Enabled)
	d.Toggle.Set(true)
	check(d.Submit.Enabled)
	d.Toggle.Set(false)
	check(!d.Submit.Enabled)
	fmt.Println("OK mediator")
}
