package main

import (
	"fmt"
	"sync"
)

func check(ok bool) {
	if !ok {
		panic("check failed")
	}
}

type Settings struct{ mode string }

var once sync.Once
var settings *Settings

func SharedSettings() *Settings {
	once.Do(func() { settings = &Settings{mode: "demo"} })
	return settings
}
func (s *Settings) Mode() string { return s.mode }

func main() {
	check(SharedSettings() == SharedSettings())
	check(SharedSettings().Mode() == "demo")
	fmt.Println("OK singleton")
}
