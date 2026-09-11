from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

class Item(Protocol):
    def total(self) -> int: ...

@dataclass(frozen=True)
class LineItem:
    value: int
    def total(self) -> int:
        return self.value

@dataclass(frozen=True)
class Bundle:
    children: tuple[Item, ...]
    def total(self) -> int:
        return sum(child.total() for child in self.children)


if __name__ == "__main__":
    root = Bundle((LineItem(10), Bundle((LineItem(20), LineItem(30)))))
    assert root.total() == 60
    assert Bundle(()).total() == 0
    print("OK composite")
