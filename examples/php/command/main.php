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

final class Counter { public int $value = 0; }
final class AddCommand {
    private string $phase = 'new'; private int $before = 0;
    public function __construct(private Counter $counter, private int $delta) {}
    public function execute(): void {
        if ($this->phase !== 'new') { throw new LogicException('execute once'); }
        $this->before = $this->counter->value; $this->counter->value += $this->delta; $this->phase = 'done';
    }
    public function undo(): void {
        if ($this->phase !== 'done') { throw new LogicException('nothing to undo'); }
        $this->counter->value = $this->before; $this->phase = 'undone';
    }
}

$counter = new Counter(); $command = new AddCommand($counter, 3);
expectError(fn() => $command->undo());
$command->execute(); check($counter->value === 3);
expectError(fn() => $command->execute());
$command->undo(); check($counter->value === 0);
expectError(fn() => $command->undo());
echo "OK command\n";
