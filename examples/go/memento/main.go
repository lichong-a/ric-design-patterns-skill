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

type identity struct{ marker byte }
type Snapshot struct {
	owner *identity
	text  string
}
type Editor struct {
	owner *identity
	Text  string
}

func NewEditor() *Editor         { return &Editor{owner: &identity{marker: 1}} }
func (e *Editor) Save() Snapshot { return Snapshot{e.owner, e.Text} }
func (e *Editor) Restore(s Snapshot) error {
	if s.owner != e.owner {
		return errors.New("foreign snapshot")
	}
	e.Text = s.text
	return nil
}

func main() {
	a, b := NewEditor(), NewEditor()
	a.Text = "one"
	saved := a.Save()
	a.Text = "two"
	check(a.Restore(saved) == nil && a.Text == "one")
	check(b.Restore(saved) != nil)
	fmt.Println("OK memento")
}
