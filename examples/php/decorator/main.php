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

interface Text { public function render(): string; }
final class PlainText implements Text { public function render(): string { return 'hi'; } }
final readonly class PrefixText implements Text {
    public function __construct(private Text $inner) {}
    public function render(): string { return '!' . $this->inner->render(); }
}
final readonly class BracketText implements Text {
    public function __construct(private Text $inner) {}
    public function render(): string { return '[' . $this->inner->render() . ']'; }
}

check((new BracketText(new PrefixText(new PlainText())))->render() === '[!hi]');
check((new PrefixText(new BracketText(new PlainText())))->render() === '![hi]');
echo "OK decorator\n";
