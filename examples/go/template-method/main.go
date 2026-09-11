package main

import (
	"fmt"
	"strings"
)

func check(ok bool) {
	if !ok {
		panic("check failed")
	}
}

type Parser interface{ Parse(string) string }
type UpperImporter struct{}

func (UpperImporter) Parse(s string) string { return strings.ToUpper(s) }
func RunImport(parser Parser, raw string) string {
	return "<" + parser.Parse(strings.TrimSpace(raw)) + ">"
}

func main() {
	check(RunImport(UpperImporter{}, " hello ") == "<HELLO>")
	check(RunImport(UpperImporter{}, "   ") == "<>")
	fmt.Println("OK template-method")
}
