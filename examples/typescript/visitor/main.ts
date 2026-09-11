export {};

function check(condition: boolean, message = "contract failed"): void {
  if (!condition) throw new Error(message);
}
function expectThrows(action: () => unknown): void {
  let failed = false;
  try { action(); } catch { failed = true; }
  check(failed, "expected an error");
}

interface NodeVisitor {
  visitText(node: TextNode): string;
  visitNumber(node: NumberNode): string;
}
interface Node { accept(visitor: NodeVisitor): string; }
class TextNode implements Node {
  constructor(readonly value: string) {}
  accept(visitor: NodeVisitor): string { return visitor.visitText(this); }
}
class NumberNode implements Node {
  constructor(readonly value: number) {}
  accept(visitor: NodeVisitor): string { return visitor.visitNumber(this); }
}
class RenderVisitor implements NodeVisitor {
  visitText(node: TextNode): string { return "text:" + node.value; }
  visitNumber(node: NumberNode): string { return `number:${node.value}`; }
}

const visitor = new RenderVisitor();
const nodes: Node[] = [new TextNode("a"), new NumberNode(7)];
check(nodes.map(node => node.accept(visitor)).join(",") === "text:a,number:7");
console.log("OK visitor");
