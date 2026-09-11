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

type Inventory struct{}

func (Inventory) Reserve(quantity int) (string, error) {
	if quantity <= 0 {
		return "", errors.New("positive quantity required")
	}
	return fmt.Sprintf("reserved:%d", quantity), nil
}

type Receipts struct{}

func (Receipts) Create(reservation string) string { return "receipt:" + reservation }

type Checkout struct {
	inventory Inventory
	receipts  Receipts
}

func (c Checkout) Place(quantity int) (string, error) {
	reserved, err := c.inventory.Reserve(quantity)
	if err != nil {
		return "", err
	}
	return c.receipts.Create(reserved), nil
}

func main() {
	checkout := Checkout{}
	result, err := checkout.Place(2)
	check(err == nil && result == "receipt:reserved:2")
	_, err = checkout.Place(0)
	check(err != nil)
	fmt.Println("OK facade")
}
