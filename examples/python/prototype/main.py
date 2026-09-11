from __future__ import annotations

from dataclasses import dataclass
from copy import deepcopy

@dataclass
class Document:
    paragraphs: list[list[str]]

    def clone(self) -> Document:
        return deepcopy(self)


if __name__ == "__main__":
    original = Document([["draft"]])
    copy = original.clone()
    copy.paragraphs[0].append("edited")
    assert original.paragraphs == [["draft"]]
    assert copy.paragraphs == [["draft", "edited"]]
    assert copy is not original
    print("OK prototype")
