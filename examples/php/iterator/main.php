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

final class Bag implements IteratorAggregate {
    /** @param list<int> $values */
    public function __construct(private array $values) {}
    public function getIterator(): Traversable { foreach ($this->values as $value) { yield $value; } }
}

$bag = new Bag([1, 2, 3]); $a = $bag->getIterator(); $b = $bag->getIterator();
check($a->current() === 1); $a->next(); check($a->current() === 2 && $b->current() === 1);
check(iterator_to_array($bag) === [1, 2, 3]);
check(iterator_to_array(new Bag([])) === []);
echo "OK iterator\n";
