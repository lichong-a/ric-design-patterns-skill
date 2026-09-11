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

interface Item { public function total(): int; }
final readonly class LineItem implements Item {
    public function __construct(private int $price) {
        if ($price < 0) { throw new InvalidArgumentException('price'); }
    }
    public function total(): int { return $this->price; }
}
final class Bundle implements Item {
    /** @param list<Item> $children */
    public function __construct(private array $children) {
        foreach ($children as $child) {
            if (!$child instanceof Item) { throw new InvalidArgumentException('child'); }
        }
    }
    public function total(): int { $result = 0; foreach ($this->children as $child) { $result += $child->total(); } return $result; }
}

$root = new Bundle([new LineItem(10), new Bundle([new LineItem(20), new LineItem(30)])]);
check($root->total() === 60 && (new Bundle([]))->total() === 0);
expectError(fn() => new Bundle([null]));
echo "OK composite\n";
