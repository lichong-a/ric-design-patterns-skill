from __future__ import annotations

from collections.abc import Callable

class Toggle:
    def __init__(self, changed: Callable[[bool], None]) -> None:
        self._changed = changed
    def select(self, value: bool) -> None:
        self._changed(value)

class SubmitButton:
    def __init__(self) -> None:
        self.enabled = False

class Dialog:
    def __init__(self) -> None:
        self.button = SubmitButton()
        self.toggle = Toggle(self.changed)
    def changed(self, selected: bool) -> None:
        self.button.enabled = selected


if __name__ == "__main__":
    dialog = Dialog()
    assert not dialog.button.enabled
    dialog.toggle.select(True)
    assert dialog.button.enabled
    dialog.toggle.select(False)
    assert not dialog.button.enabled
    print("OK mediator")
