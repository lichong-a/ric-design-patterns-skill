from __future__ import annotations

from collections.abc import Iterable, Iterator

class Bag:
    def __init__(self, values: Iterable[int]) -> None:
        self._values = tuple(values)
    def __iter__(self) -> Iterator[int]:
        return iter(self._values)


if __name__ == "__main__":
    bag = Bag([1, 2, 3])
    a, b = iter(bag), iter(bag)
    assert next(a) == 1
    assert next(a) == 2
    assert next(b) == 1
    assert list(bag) == [1, 2, 3]
    assert list(Bag([])) == []
    print("OK iterator")
