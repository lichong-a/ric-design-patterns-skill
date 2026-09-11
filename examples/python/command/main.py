from __future__ import annotations

from dataclasses import dataclass

@dataclass
class Counter:
    value: int = 0

class AddCommand:
    def __init__(self, counter: Counter, amount: int) -> None:
        self._counter = counter
        self._amount = amount
        self._before = 0
        self._phase = "new"
    def execute(self) -> None:
        if self._phase != "new":
            raise RuntimeError("command already executed")
        self._before = self._counter.value
        self._counter.value += self._amount
        self._phase = "done"
    def undo(self) -> None:
        if self._phase != "done":
            raise RuntimeError("nothing to undo")
        self._counter.value = self._before
        self._phase = "undone"


if __name__ == "__main__":
    counter = Counter()
    command = AddCommand(counter, 5)
    command.execute()
    assert counter.value == 5
    try:
        command.execute()
    except RuntimeError:
        pass
    else:
        raise AssertionError("duplicate execution accepted")
    command.undo()
    assert counter.value == 0
    try:
        command.undo()
    except RuntimeError:
        pass
    else:
        raise AssertionError("duplicate undo accepted")
    print("OK command")
