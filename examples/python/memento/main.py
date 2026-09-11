from __future__ import annotations

from dataclasses import dataclass

@dataclass(frozen=True)
class Snapshot:
    _owner: object
    _text: str

class Editor:
    def __init__(self, text: str) -> None:
        self._text = text
        self._owner = object()
    @property
    def text(self) -> str:
        return self._text
    def write(self, text: str) -> None:
        self._text = text
    def save(self) -> Snapshot:
        return Snapshot(self._owner, self._text)
    def restore(self, snapshot: Snapshot) -> None:
        if snapshot._owner is not self._owner:
            raise ValueError("foreign snapshot")
        self._text = snapshot._text


if __name__ == "__main__":
    editor = Editor("draft")
    history = editor.save()
    editor.write("edited")
    editor.restore(history)
    assert editor.text == "draft"
    try:
        Editor("other").restore(history)
    except ValueError:
        pass
    else:
        raise AssertionError("foreign snapshot accepted")
    print("OK memento")
