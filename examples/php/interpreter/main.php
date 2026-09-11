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

interface Expr { /** @param array<string, int> $context */ public function evaluate(array $context): int; }
final readonly class Literal implements Expr {
    public function __construct(private int $value) {}
    public function evaluate(array $context): int { return $this->value; }
}
final readonly class Variable implements Expr {
    public function __construct(private string $name) {}
    public function evaluate(array $context): int {
        if (!array_key_exists($this->name, $context) || !is_int($context[$this->name])) { throw new InvalidArgumentException('unknown or invalid variable'); }
        return $context[$this->name];
    }
}
final readonly class Add implements Expr {
    public function __construct(private Expr $left, private Expr $right) {}
    public function evaluate(array $context): int { return $this->left->evaluate($context) + $this->right->evaluate($context); }
}

$expr = new Add(new Variable('x'), new Literal(2));
check($expr->evaluate(['x' => 3]) === 5);
expectError(fn() => $expr->evaluate([]));
expectError(fn() => $expr->evaluate(['x' => '3']));
echo "OK interpreter\n";
