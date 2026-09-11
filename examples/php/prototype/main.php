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

final class Paragraph {
    public function __construct(public string $text) {}
}
final class Document {
    /** @param list<Paragraph> $paragraphs */
    public function __construct(public string $title, public array $paragraphs) {}
    public function __clone(): void {
        $this->paragraphs = array_map(fn(Paragraph $p): Paragraph => clone $p, $this->paragraphs);
    }
}

$original = new Document('Design', [new Paragraph('one')]);
$copy = clone $original;
$copy->paragraphs[0]->text = 'changed';
$copy->paragraphs[] = new Paragraph('two');
check($original->paragraphs[0]->text === 'one');
check(count($original->paragraphs) === 1 && count($copy->paragraphs) === 2);
echo "OK prototype\n";
