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

interface Button { public function draw(): string; }
interface Checkbox { public function mark(): string; }
final readonly class ThemedButton implements Button {
    public function __construct(private string $theme) {}
    public function draw(): string { return $this->theme . ':button'; }
}
final readonly class ThemedCheckbox implements Checkbox {
    public function __construct(private string $theme) {}
    public function mark(): string { return $this->theme . ':checkbox'; }
}
interface WidgetFactory { public function button(): Button; public function checkbox(): Checkbox; }
final class LightFactory implements WidgetFactory {
    public function button(): Button { return new ThemedButton('light'); }
    public function checkbox(): Checkbox { return new ThemedCheckbox('light'); }
}
final class DarkFactory implements WidgetFactory {
    public function button(): Button { return new ThemedButton('dark'); }
    public function checkbox(): Checkbox { return new ThemedCheckbox('dark'); }
}
function screen(WidgetFactory $f): string { return $f->button()->draw() . '/' . $f->checkbox()->mark(); }

check(screen(new LightFactory()) === 'light:button/light:checkbox');
check(screen(new DarkFactory()) === 'dark:button/dark:checkbox');
echo "OK abstract-factory\n";
