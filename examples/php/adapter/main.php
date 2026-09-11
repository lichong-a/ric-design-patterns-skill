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

final class LegacySensor { public function centimeters(): int { return 250; } }
interface MeterReader { public function meters(): float; }
final readonly class SensorAdapter implements MeterReader {
    public function __construct(private LegacySensor $sensor) {}
    public function meters(): float { return $this->sensor->centimeters() / 100.0; }
}

$reader = new SensorAdapter(new LegacySensor());
check($reader->meters() === 2.5);
echo "OK adapter\n";
