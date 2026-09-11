package main

import (
	"fmt"
)

func check(ok bool) {
	if !ok {
		panic("check failed")
	}
}

type Channel interface{ Send(string) string }
type EmailChannel struct{}

func (EmailChannel) Send(s string) string { return "email:" + s }

type SmsChannel struct{}

func (SmsChannel) Send(s string) string { return "sms:" + s }

type Notice struct{ channel Channel }

func (n Notice) Deliver(s string) string { return n.channel.Send(s) }

type UrgentNotice struct{ Notice }

func (n UrgentNotice) Deliver(s string) string { return n.channel.Send("!" + s) }

func main() {
	check((Notice{EmailChannel{}}).Deliver("hi") == "email:hi")
	check((UrgentNotice{Notice{SmsChannel{}}}).Deliver("hi") == "sms:!hi")
	fmt.Println("OK bridge")
}
