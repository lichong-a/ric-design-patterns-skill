from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Protocol

class Renderer(Protocol):
    def render(self) -> str: ...

class PlainRenderer:
    def render(self) -> str:
        return "plain"

class JsonRenderer:
    def render(self) -> str:
        return '{"format":"json"}'

class Publisher(ABC):
    @abstractmethod
    def make(self) -> Renderer:
        raise NotImplementedError

    def publish(self) -> str:
        return "published:" + self.make().render()

class PlainPublisher(Publisher):
    def make(self) -> Renderer:
        return PlainRenderer()

class JsonPublisher(Publisher):
    def make(self) -> Renderer:
        return JsonRenderer()


if __name__ == "__main__":
    assert PlainPublisher().publish() == "published:plain"
    assert JsonPublisher().publish() == 'published:{"format":"json"}'
    print("OK factory-method")
