package main

import (
	"fmt"
)

func check(ok bool) {
	if !ok {
		panic("check failed")
	}
}

type NodeVisitor interface {
	VisitText(TextNode) string
	VisitNumber(NumberNode) string
}
type Node interface{ Accept(NodeVisitor) string }
type TextNode struct{ Value string }

func (n TextNode) Accept(v NodeVisitor) string { return v.VisitText(n) }

type NumberNode struct{ Value int }

func (n NumberNode) Accept(v NodeVisitor) string { return v.VisitNumber(n) }

type RenderVisitor struct{}

func (RenderVisitor) VisitText(n TextNode) string     { return "text:" + n.Value }
func (RenderVisitor) VisitNumber(n NumberNode) string { return fmt.Sprintf("number:%d", n.Value) }

func main() {
	v := RenderVisitor{}
	check((TextNode{"a"}).Accept(v) == "text:a")
	check((NumberNode{7}).Accept(v) == "number:7")
	fmt.Println("OK visitor")
}
