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

interface GateState { public function isOpen(): bool; public function coin(): GateState; public function enter(): GateState; }
final class Locked implements GateState {
    public function isOpen(): bool { return false; }
    public function coin(): GateState { return new Unlocked(); }
    public function enter(): GateState { return $this; }
}
final class Unlocked implements GateState {
    public function isOpen(): bool { return true; }
    public function coin(): GateState { return $this; }
    public function enter(): GateState { return new Locked(); }
}
final class Gate {
    private GateState $state;
    public function __construct() { $this->state = new Locked(); }
    public function isOpen(): bool { return $this->state->isOpen(); }
    public function coin(): void { $this->state = $this->state->coin(); }
    public function enter(): void { $this->state = $this->state->enter(); }
}

$gate = new Gate(); check(!$gate->isOpen());
$gate->enter(); check(!$gate->isOpen());
$gate->coin(); check($gate->isOpen());
$gate->coin(); check($gate->isOpen());
$gate->enter(); check(!$gate->isOpen());
echo "OK state\n";
