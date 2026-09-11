from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

class NodeVisitor(Protocol):
    def visit_text(self, node: TextNode) -> str: ...
    def visit_number(self, node: NumberNode) -> str: ...

class Node(Protocol):
    def accept(self, visitor: NodeVisitor) -> str: ...

@dataclass(frozen=True)
class TextNode:
    value: str
    def accept(self, visitor: NodeVisitor) -> str:
        return visitor.visit_text(self)

@dataclass(frozen=True)
class NumberNode:
    value: int
    def accept(self, visitor: NodeVisitor) -> str:
        return visitor.visit_number(self)

class RenderVisitor:
    def visit_text(self, node: TextNode) -> str:
        return "text:" + node.value
    def visit_number(self, node: NumberNode) -> str:
        return f"number:{node.value}"


if __name__ == "__main__":
    visitor = RenderVisitor()
    nodes: list[Node] = [TextNode("a"), NumberNode(7)]
    assert [node.accept(visitor) for node in nodes] == ["text:a", "number:7"]
    print("OK visitor")
