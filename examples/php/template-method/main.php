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

abstract class Importer {
    abstract protected function parse(string $value): string;
    final public function run(string $raw): string { return '<' . $this->parse(trim($raw)) . '>'; }
}
final class UpperImporter extends Importer { protected function parse(string $value): string { return strtoupper($value); } }

check((new UpperImporter())->run(' hello ') === '<HELLO>');
check((new UpperImporter())->run('   ') === '<>');
echo "OK template-method\n";
