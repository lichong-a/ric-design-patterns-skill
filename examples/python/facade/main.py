from __future__ import annotations

class Inventory:
    def reserve(self, quantity: int) -> str:
        if quantity <= 0:
            raise ValueError("quantity must be positive")
        return f"reserved:{quantity}"

class Receipts:
    def create(self, reservation: str) -> str:
        return "receipt:" + reservation

class Checkout:
    def __init__(self, inventory: Inventory, receipts: Receipts) -> None:
        self._inventory = inventory
        self._receipts = receipts
    def place(self, quantity: int) -> str:
        reservation = self._inventory.reserve(quantity)
        return self._receipts.create(reservation)


if __name__ == "__main__":
    checkout = Checkout(Inventory(), Receipts())
    assert checkout.place(2) == "receipt:reserved:2"
    try:
        checkout.place(0)
    except ValueError:
        pass
    else:
        raise AssertionError("invalid order accepted")
    print("OK facade")
