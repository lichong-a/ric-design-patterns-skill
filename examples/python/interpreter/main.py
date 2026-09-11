from __future__ import annotations

from dataclasses import dataclass
from collections.abc import Mapping
from typing import Protocol

class Expr(Protocol):
    def evaluate(self, context: Mapping[str, int]) -> int: ...

@dataclass(frozen=True)
class Literal:
    value: int
    def evaluate(self, context: Mapping[str, int]) -> int:
        return self.value

@dataclass(frozen=True)
class Variable:
    name: str
    def evaluate(self, context: Mapping[str, int]) -> int:
        return context[self.name]

@dataclass(frozen=True)
class Add:
    left: Expr
    right: Expr
    def evaluate(self, context: Mapping[str, int]) -> int:
        return self.left.evaluate(context) + self.right.evaluate(context)


if __name__ == "__main__":
    expr = Add(Variable("x"), Literal(2))
    assert expr.evaluate({"x": 3}) == 5
    try:
        expr.evaluate({})
    except KeyError:
        pass
    else:
        raise AssertionError("missing variable accepted")
    print("OK interpreter")
