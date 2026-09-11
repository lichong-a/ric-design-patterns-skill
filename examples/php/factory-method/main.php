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

interface Renderer { public function render(): string; }
final class PlainRenderer implements Renderer { public function render(): string { return 'plain'; } }
final class JsonRenderer implements Renderer { public function render(): string { return 'json'; } }
abstract class Publisher {
    abstract protected function make(): Renderer;
    final public function publish(): string { return 'published:' . $this->make()->render(); }
}
final class PlainPublisher extends Publisher { protected function make(): Renderer { return new PlainRenderer(); } }
final class JsonPublisher extends Publisher { protected function make(): Renderer { return new JsonRenderer(); } }

check((new PlainPublisher())->publish() === 'published:plain');
check((new JsonPublisher())->publish() === 'published:json');
echo "OK factory-method\n";
