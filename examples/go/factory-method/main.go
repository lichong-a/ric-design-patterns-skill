package main

import (
	"fmt"
)

func check(ok bool) {
	if !ok {
		panic("check failed")
	}
}

type Renderer interface{ Render() string }
type PlainRenderer struct{}

func (PlainRenderer) Render() string { return "plain" }

type JsonRenderer struct{}

func (JsonRenderer) Render() string { return "json" }

type Creator interface{ Make() Renderer }
type PlainPublisher struct{}

func (PlainPublisher) Make() Renderer { return PlainRenderer{} }

type JsonPublisher struct{}

func (JsonPublisher) Make() Renderer { return JsonRenderer{} }
func Publish(c Creator) string       { return "published:" + c.Make().Render() }

func main() {
	check(Publish(PlainPublisher{}) == "published:plain")
	check(Publish(JsonPublisher{}) == "published:json")
	fmt.Println("OK factory-method")
}
