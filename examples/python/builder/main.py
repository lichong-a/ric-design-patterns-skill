from __future__ import annotations

from dataclasses import dataclass

@dataclass(frozen=True)
class Report:
    title: str
    sections: tuple[str, ...]

class ReportBuilder:
    def __init__(self) -> None:
        self._title = ""
        self._sections: list[str] = []

    def title(self, value: str) -> ReportBuilder:
        self._title = value.strip()
        return self

    def add(self, section: str) -> ReportBuilder:
        self._sections.append(section)
        return self

    def build(self) -> Report:
        if not self._title:
            raise ValueError("title is required")
        return Report(self._title, tuple(self._sections))


if __name__ == "__main__":
    builder = ReportBuilder().title("Design").add("Intent")
    report = builder.build()
    builder.add("Trade-offs")
    assert report.sections == ("Intent",)
    try:
        ReportBuilder().build()
    except ValueError:
        pass
    else:
        raise AssertionError("empty title accepted")
    print("OK builder")
