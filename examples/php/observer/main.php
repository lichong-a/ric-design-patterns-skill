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

final class Events {
    private int $sequence = 0;
    /** @var array<int, Closure> */
    private array $listeners = [];
    public function subscribe(Closure $listener): int { $id = ++$this->sequence; $this->listeners[$id] = $listener; return $id; }
    public function unsubscribe(int $id): void { unset($this->listeners[$id]); }
    public function emit(int $value): void { $snapshot = $this->listeners; foreach ($snapshot as $listener) { $listener($value); } }
}

$events = new Events(); $seen = [];
$token = $events->subscribe(function(int $n) use (&$seen): void { $seen[] = $n; });
$events->emit(1); $events->unsubscribe($token); $events->emit(2);
check($seen === [1]);
$self = 0; $self = $events->subscribe(function(int $n) use ($events, &$self): void { $events->unsubscribe($self); });
$events->emit(3); $events->emit(4);
echo "OK observer\n";
