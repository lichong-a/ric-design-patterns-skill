from __future__ import annotations

from typing import Protocol

class Length(Protocol):
    def meters(self) -> float: ...

class LegacyMeter:
    def centimeters(self) -> float:
        return 250.0

class MeterAdapter:
    def __init__(self, legacy: LegacyMeter) -> None:
        self._legacy = legacy

    def meters(self) -> float:
        return self._legacy.centimeters() / 100.0


if __name__ == "__main__":
    length: Length = MeterAdapter(LegacyMeter())
    assert length.meters() == 2.5
    print("OK adapter")
