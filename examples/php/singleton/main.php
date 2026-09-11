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

final class Settings {
    private static ?self $instance = null;
    private function __construct() {}
    private function __clone() {}
    public static function instance(): self { return self::$instance ??= new self(); }
    public function mode(): string { return 'demo'; }
    public function __serialize(): array { throw new LogicException('serialization disabled'); }
    public function __unserialize(array $data): void { throw new LogicException('serialization disabled'); }
}

check(Settings::instance() === Settings::instance());
check(Settings::instance()->mode() === 'demo');
expectError(fn() => serialize(Settings::instance()));
echo "OK singleton\n";
