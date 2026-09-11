from __future__ import annotations

from dataclasses import dataclass

@dataclass(frozen=True)
class Style:
    font: str

class StylePool:
    def __init__(self) -> None:
        self._styles: dict[str, Style] = {}
    def get(self, font: str) -> Style:
        if font not in self._styles:
            self._styles[font] = Style(font)
        return self._styles[font]

@dataclass(frozen=True)
class Glyph:
    character: str
    x: int
    style: Style


if __name__ == "__main__":
    pool = StylePool()
    a = Glyph("a", 0, pool.get("mono"))
    b = Glyph("b", 10, pool.get("mono"))
    assert a.style is b.style
    assert a.x != b.x
    assert pool.get("serif") is not a.style
    print("OK flyweight")
