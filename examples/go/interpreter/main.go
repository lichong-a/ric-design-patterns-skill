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

type Context map[string]int
type Expr interface{ Eval(Context) (int, error) }
type Literal struct{ value int }

func (e Literal) Eval(Context) (int, error) { return e.value, nil }

type Variable struct{ name string }

func (e Variable) Eval(c Context) (int, error) {
	value, ok := c[e.name]
	if !ok {
		return 0, errors.New("unknown variable: " + e.name)
	}
	return value, nil
}

type Add struct{ left, right Expr }

func (e Add) Eval(c Context) (int, error) {
	left, err := e.left.Eval(c)
	if err != nil {
		return 0, err
	}
	right, err := e.right.Eval(c)
	if err != nil {
		return 0, err
	}
	return left + right, nil
}

func main() {
	expr := Add{Variable{"x"}, Literal{2}}
	value, err := expr.Eval(Context{"x": 3})
	check(err == nil && value == 5)
	_, err = expr.Eval(Context{})
	check(err != nil)
	fmt.Println("OK interpreter")
}
