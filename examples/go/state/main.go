package main

import (
	"fmt"
)

func check(ok bool) {
	if !ok {
		panic("check failed")
	}
}

type GateState interface {
	Open() bool
	Coin() GateState
	Enter() GateState
}
type Locked struct{}

func (Locked) Open() bool         { return false }
func (Locked) Coin() GateState    { return Unlocked{} }
func (s Locked) Enter() GateState { return s }

type Unlocked struct{}

func (Unlocked) Open() bool        { return true }
func (s Unlocked) Coin() GateState { return s }
func (Unlocked) Enter() GateState  { return Locked{} }

type Gate struct{ state GateState }

func NewGate() *Gate   { return &Gate{state: Locked{}} }
func (g *Gate) Coin()  { g.state = g.state.Coin() }
func (g *Gate) Enter() { g.state = g.state.Enter() }

func main() {
	g := NewGate()
	check(!g.state.Open())
	g.Enter()
	check(!g.state.Open())
	g.Coin()
	check(g.state.Open())
	g.Coin()
	check(g.state.Open())
	g.Enter()
	check(!g.state.Open())
	fmt.Println("OK state")
}
