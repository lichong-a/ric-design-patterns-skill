from __future__ import annotations

from typing import Protocol

class GateState(Protocol):
    name: str
    def coin(self) -> GateState: ...
    def enter(self) -> GateState: ...

class Locked:
    name = "locked"
    def coin(self) -> GateState:
        return Unlocked()
    def enter(self) -> GateState:
        return self

class Unlocked:
    name = "unlocked"
    def coin(self) -> GateState:
        return self
    def enter(self) -> GateState:
        return Locked()

class Gate:
    def __init__(self) -> None:
        self.state: GateState = Locked()
    def coin(self) -> None:
        self.state = self.state.coin()
    def enter(self) -> None:
        self.state = self.state.enter()


if __name__ == "__main__":
    gate = Gate()
    assert gate.state.name == "locked"
    gate.enter()
    assert gate.state.name == "locked"
    gate.coin()
    assert gate.state.name == "unlocked"
    gate.enter()
    assert gate.state.name == "locked"
    print("OK state")
