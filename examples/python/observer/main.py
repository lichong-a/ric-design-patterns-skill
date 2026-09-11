from __future__ import annotations

from collections.abc import Callable

class Events:
    def __init__(self) -> None:
        self._listeners: dict[int, Callable[[int], None]] = {}
        self._next = 0
    def subscribe(self, listener: Callable[[int], None]) -> int:
        self._next += 1
        self._listeners[self._next] = listener
        return self._next
    def unsubscribe(self, token: int) -> None:
        self._listeners.pop(token, None)
    def emit(self, value: int) -> None:
        # Snapshot: changes to subscriptions affect the next emission.
        for listener in tuple(self._listeners.values()):
            listener(value)


if __name__ == "__main__":
    events = Events()
    seen: list[int] = []
    token = events.subscribe(seen.append)
    events.emit(3)
    events.unsubscribe(token)
    events.emit(9)
    assert seen == [3]
    # Unsubscribing during dispatch does not invalidate the current snapshot.
    late: list[int] = []
    other = events.subscribe(late.append)
    events.subscribe(lambda value: events.unsubscribe(other))
    events.emit(1)
    events.emit(2)
    assert late == [1]
    print("OK observer")
