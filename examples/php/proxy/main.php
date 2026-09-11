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

interface Image { public function read(): string; }
final class RealImage implements Image { public function read(): string { return 'pixels'; } }
final class LazyImage implements Image {
    private ?RealImage $real = null;
    private int $loads = 0;
    public function loads(): int { return $this->loads; }
    public function read(): string {
        if ($this->real === null) { $this->real = new RealImage(); ++$this->loads; }
        return $this->real->read();
    }
}

$image = new LazyImage(); check($image->loads() === 0);
check($image->read() === 'pixels' && $image->read() === 'pixels');
check($image->loads() === 1);
echo "OK proxy\n";
