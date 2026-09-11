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

final readonly class Rule {
    public function __construct(private Closure $accepts, private ?Rule $next = null) {}
    public function handle(int $value): bool { return ($this->accepts)($value) && ($this->next?->handle($value) ?? true); }
}

$visits = 0;
$chain = new Rule(fn(int $n): bool => $n > 0, new Rule(function(int $n) use (&$visits): bool { ++$visits; return $n < 10; }));
check(!$chain->handle(-1) && $visits === 0);
check($chain->handle(5) && $visits === 1);
check(!$chain->handle(12) && $visits === 2);
echo "OK chain-of-responsibility\n";
