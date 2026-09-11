package main

import (
	"errors"
	"fmt"
	"strings"
)

func check(ok bool) {
	if !ok {
		panic("check failed")
	}
}

type Report struct {
	Title    string
	Sections []string
}
type ReportBuilder struct {
	title    string
	sections []string
}

func (b *ReportBuilder) Title(v string) *ReportBuilder { b.title = strings.TrimSpace(v); return b }
func (b *ReportBuilder) Section(v string) *ReportBuilder {
	b.sections = append(b.sections, v)
	return b
}
func (b *ReportBuilder) Build() (Report, error) {
	if b.title == "" {
		return Report{}, errors.New("title required")
	}
	return Report{b.title, append([]string(nil), b.sections...)}, nil
}

func main() {
	b := &ReportBuilder{}
	_, err := b.Build()
	check(err != nil)
	first, err := b.Title("Design").Section("Intent").Build()
	check(err == nil)
	b.Section("Tests")
	second, err := b.Build()
	check(err == nil)
	first.Sections[0] = "changed"
	check(len(first.Sections) == 1 && len(second.Sections) == 2)
	check(second.Sections[0] == "Intent")
	fmt.Println("OK builder")
}
