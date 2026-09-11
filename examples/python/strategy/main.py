from __future__ import annotations

from collections.abc import Callable

class Pricing:
    def __init__(self, discount: Callable[[int], int]) -> None:
        self._discount = discount
    def total(self, base: int) -> int:
        if base < 0:
            raise ValueError("base must be non-negative")
        return self._discount(base)


if __name__ == "__main__":
    assert Pricing(lambda amount: max(0, amount - 10)).total(100) == 90
    assert Pricing(lambda amount: max(0, amount - 20)).total(100) == 80
    assert Pricing(lambda amount: max(0, amount - 20)).total(5) == 0
    print("OK strategy")
