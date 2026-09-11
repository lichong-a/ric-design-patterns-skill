from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

class Text(Protocol):
    def read(self) -> str: ...

@dataclass(frozen=True)
class PlainText:
    value: str
    def read(self) -> str:
        return self.value

@dataclass(frozen=True)
class PrefixText:
    inner: Text
    def read(self) -> str:
        return "!" + self.inner.read()

@dataclass(frozen=True)
class BracketText:
    inner: Text
    def read(self) -> str:
        return "[" + self.inner.read() + "]"


if __name__ == "__main__":
    assert BracketText(PrefixText(PlainText("hi"))).read() == "[!hi]"
    assert PrefixText(BracketText(PlainText("hi"))).read() == "![hi]"
    print("OK decorator")
