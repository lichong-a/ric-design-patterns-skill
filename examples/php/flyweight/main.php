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

final readonly class Style { public function __construct(public string $font) {} }
final class StylePool {
    /** @var array<string, Style> */
    private array $cache = [];
    public function get(string $font): Style { return $this->cache[$font] ??= new Style($font); }
}
final readonly class Glyph { public function __construct(public string $character, public int $x, public Style $style) {} }

$pool = new StylePool();
$a = new Glyph('a', 1, $pool->get('mono')); $b = new Glyph('b', 8, $pool->get('mono'));
check($a->style === $b->style && $a->x !== $b->x);
check($pool->get('serif') !== $a->style);
echo "OK flyweight\n";
