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

final class Pricing {
    public function __construct(public Closure $rule) {}
    public function quote(int $base): int {
        if ($base < 0) { throw new InvalidArgumentException('base'); }
        return ($this->rule)($base);
    }
}
function discount(int $amount): Closure { return fn(int $base): int => max(0, $base - $amount); }

$pricing = new Pricing(discount(10)); check($pricing->quote(100) === 90);
$pricing->rule = discount(20);
check($pricing->quote(100) === 80 && $pricing->quote(5) === 0);
expectError(fn() => $pricing->quote(-1));
echo "OK strategy\n";
