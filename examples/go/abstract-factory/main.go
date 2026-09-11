package main

import (
	"fmt"
)

func check(ok bool) {
	if !ok {
		panic("check failed")
	}
}

type Button interface{ Draw() string }
type Checkbox interface{ Mark() string }
type ThemedButton struct{ theme string }

func (b ThemedButton) Draw() string { return b.theme + ":button" }

type ThemedCheckbox struct{ theme string }

func (c ThemedCheckbox) Mark() string { return c.theme + ":checkbox" }

type WidgetFactory interface {
	Button() Button
	Checkbox() Checkbox
}
type LightFactory struct{}

func (LightFactory) Button() Button     { return ThemedButton{"light"} }
func (LightFactory) Checkbox() Checkbox { return ThemedCheckbox{"light"} }

type DarkFactory struct{}

func (DarkFactory) Button() Button     { return ThemedButton{"dark"} }
func (DarkFactory) Checkbox() Checkbox { return ThemedCheckbox{"dark"} }
func Screen(f WidgetFactory) string    { return f.Button().Draw() + "/" + f.Checkbox().Mark() }

func main() {
	check(Screen(LightFactory{}) == "light:button/light:checkbox")
	check(Screen(DarkFactory{}) == "dark:button/dark:checkbox")
	fmt.Println("OK abstract-factory")
}
