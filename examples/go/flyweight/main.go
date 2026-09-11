package main

import (
	"fmt"
)

func check(ok bool) {
	if !ok {
		panic("check failed")
	}
}

type Style struct{ font string }
type StylePool struct{ cache map[string]*Style }

func NewStylePool() *StylePool { return &StylePool{cache: make(map[string]*Style)} }
func (p *StylePool) Get(font string) *Style {
	if cached, ok := p.cache[font]; ok {
		return cached
	}
	created := &Style{font: font}
	p.cache[font] = created
	return created
}

type Glyph struct {
	character rune
	x         int
	style     *Style
}

func main() {
	pool := NewStylePool()
	a, b := Glyph{'a', 1, pool.Get("mono")}, Glyph{'b', 8, pool.Get("mono")}
	check(a.style == b.style && a.x != b.x)
	check(pool.Get("serif") != a.style)
	fmt.Println("OK flyweight")
}
