from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

class Button(Protocol):
    def draw(self) -> str: ...

class Checkbox(Protocol):
    def mark(self) -> str: ...

@dataclass(frozen=True)
class ThemedButton:
    theme: str
    def draw(self) -> str:
        return self.theme + ":button"

@dataclass(frozen=True)
class ThemedCheckbox:
    theme: str
    def mark(self) -> str:
        return self.theme + ":checkbox"

class WidgetFactory(Protocol):
    def button(self) -> Button: ...
    def checkbox(self) -> Checkbox: ...

class LightFactory:
    def button(self) -> Button:
        return ThemedButton("light")
    def checkbox(self) -> Checkbox:
        return ThemedCheckbox("light")

class DarkFactory:
    def button(self) -> Button:
        return ThemedButton("dark")
    def checkbox(self) -> Checkbox:
        return ThemedCheckbox("dark")

def screen(factory: WidgetFactory) -> tuple[str, str]:
    return factory.button().draw(), factory.checkbox().mark()


if __name__ == "__main__":
    assert screen(LightFactory()) == ("light:button", "light:checkbox")
    assert screen(DarkFactory()) == ("dark:button", "dark:checkbox")
    print("OK abstract-factory")
