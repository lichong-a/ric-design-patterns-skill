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

final readonly class Snapshot {
    public function __construct(private object $owner, private string $text) {}
    public function readFor(object $owner): string {
        if ($owner !== $this->owner) { throw new InvalidArgumentException('foreign snapshot'); }
        return $this->text;
    }
}
final class Editor {
    private object $owner;
    public string $text = '';
    public function __construct() { $this->owner = new stdClass(); }
    private function __clone() {}
    public function save(): Snapshot { return new Snapshot($this->owner, $this->text); }
    public function restore(Snapshot $snapshot): void { $this->text = $snapshot->readFor($this->owner); }
}

$a = new Editor(); $b = new Editor();
$a->text = 'one'; $saved = $a->save(); $a->text = 'two';
$a->restore($saved); check($a->text === 'one');
expectError(fn() => $b->restore($saved));
echo "OK memento\n";
