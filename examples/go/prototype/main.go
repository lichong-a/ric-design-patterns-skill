package main

import (
	"fmt"
)

func check(ok bool) {
	if !ok {
		panic("check failed")
	}
}

type Document struct {
	Title      string
	Paragraphs [][]string
}

func (d Document) Clone() Document {
	rows := make([][]string, len(d.Paragraphs))
	for i, row := range d.Paragraphs {
		rows[i] = append([]string(nil), row...)
	}
	return Document{d.Title, rows}
}

func main() {
	original := Document{"Design", [][]string{{"one"}}}
	copy := original.Clone()
	copy.Paragraphs[0][0] = "changed"
	copy.Paragraphs[0] = append(copy.Paragraphs[0], "two")
	check(original.Paragraphs[0][0] == "one")
	check(len(original.Paragraphs[0]) == 1 && len(copy.Paragraphs[0]) == 2)
	fmt.Println("OK prototype")
}
