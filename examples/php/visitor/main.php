<?php
declare(strict_types=1);

function check(bool $condition): void {
    if (!$condition) { throw new RuntimeException('check failed'); }
}
function expectError(Closure $action): void {
    $failed = false;
    try { $action(); } catch (LogicException $error) { $failed = true; }
    check($failed);
}

interface NodeVisitor { public function visitText(TextNode $node): string; public function visitNumber(NumberNode $node): string; }
interface Node { public function accept(NodeVisitor $visitor): string; }
final readonly class TextNode implements Node {
    public function __construct(public string $value) {}
    public function accept(NodeVisitor $visitor): string { return $visitor->visitText($this); }
}
final readonly class NumberNode implements Node {
    public function __construct(public int $value) {}
    public function accept(NodeVisitor $visitor): string { return $visitor->visitNumber($this); }
}
final class RenderVisitor implements NodeVisitor {
    public function visitText(TextNode $node): string { return 'text:' . $node->value; }
    public function visitNumber(NumberNode $node): string { return 'number:' . $node->value; }
}

$v = new RenderVisitor();
check((new TextNode('a'))->accept($v) === 'text:a');
check((new NumberNode(7))->accept($v) === 'number:7');
echo "OK visitor\n";
