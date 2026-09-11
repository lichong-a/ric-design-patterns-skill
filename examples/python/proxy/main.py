from __future__ import annotations

from typing import Protocol

class Image(Protocol):
    def render(self) -> str: ...

class RealImage:
    def render(self) -> str:
        return "pixels"

class ImageProxy:
    def __init__(self) -> None:
        self._real: RealImage | None = None
        self.loads = 0
    def render(self) -> str:
        if self._real is None:
            self._real = RealImage()
            self.loads += 1
        return self._real.render()


if __name__ == "__main__":
    proxy = ImageProxy()
    assert proxy.loads == 0
    assert proxy.render() == "pixels"
    assert proxy.render() == "pixels"
    assert proxy.loads == 1
    print("OK proxy")
