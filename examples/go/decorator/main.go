package main

import (
	"fmt"
)

func check(ok bool) {
	if !ok {
		panic("check failed")
	}
}

type Text interface{ Render() string }
type PlainText struct{}

func (PlainText) Render() string { return "hi" }

type PrefixText struct{ inner Text }

func (t PrefixText) Render() string { return "!" + t.inner.Render() }

type BracketText struct{ inner Text }

func (t BracketText) Render() string { return "[" + t.inner.Render() + "]" }

func main() {
	check((BracketText{PrefixText{PlainText{}}}).Render() == "[!hi]")
	check((PrefixText{BracketText{PlainText{}}}).Render() == "![hi]")
	fmt.Println("OK decorator")
}
