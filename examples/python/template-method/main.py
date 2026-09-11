from __future__ import annotations

from abc import ABC, abstractmethod
from typing import final

class Importer(ABC):
    @final
    def run(self, raw: str) -> str:
        loaded = raw.strip()
        parsed = self.parse(loaded)
        return "<" + parsed + ">"
    @abstractmethod
    def parse(self, text: str) -> str:
        raise NotImplementedError

class UpperImporter(Importer):
    def parse(self, text: str) -> str:
        return text.upper()


if __name__ == "__main__":
    assert UpperImporter().run(" hello ") == "<HELLO>"
    print("OK template-method")
