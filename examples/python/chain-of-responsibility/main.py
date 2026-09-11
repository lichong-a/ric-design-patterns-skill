from __future__ import annotations

from collections.abc import Callable

class Rule:
    def __init__(self, predicate: Callable[[int], bool], next_rule: Rule | None = None) -> None:
        self._predicate = predicate
        self._next = next_rule
    def handle(self, value: int) -> bool:
        if not self._predicate(value):
            return False
        return self._next.handle(value) if self._next else True


if __name__ == "__main__":
    visits: list[int] = []
    def below_limit(value: int) -> bool:
        visits.append(value)
        return value < 1000
    chain = Rule(lambda n: n > 0, Rule(below_limit))
    assert chain.handle(100)
    assert not chain.handle(-1)
    assert visits == [100]
    assert not chain.handle(1000)
    print("OK chain-of-responsibility")
