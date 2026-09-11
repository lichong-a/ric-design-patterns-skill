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

final class Inventory {
    public function reserve(int $quantity): string {
        if ($quantity <= 0) { throw new InvalidArgumentException('positive quantity required'); }
        return 'reserved:' . $quantity;
    }
}
final class Receipts { public function create(string $reservation): string { return 'receipt:' . $reservation; } }
final readonly class Checkout {
    public function __construct(private Inventory $inventory, private Receipts $receipts) {}
    public function place(int $quantity): string { return $this->receipts->create($this->inventory->reserve($quantity)); }
}

$checkout = new Checkout(new Inventory(), new Receipts());
check($checkout->place(2) === 'receipt:reserved:2');
expectError(fn() => $checkout->place(0));
echo "OK facade\n";
