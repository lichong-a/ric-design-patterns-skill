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

final class Toggle {
    public ?Closure $changed = null;
    public function set(bool $value): void { if ($this->changed !== null) { ($this->changed)($value); } }
}
final class SubmitButton { public bool $enabled = false; }
final class Dialog {
    public Toggle $toggle; public SubmitButton $submit;
    public function __construct() {
        $this->toggle = new Toggle(); $this->submit = new SubmitButton();
        $this->toggle->changed = function(bool $value): void { $this->submit->enabled = $value; };
    }
}

$dialog = new Dialog(); check(!$dialog->submit->enabled);
$dialog->toggle->set(true); check($dialog->submit->enabled);
$dialog->toggle->set(false); check(!$dialog->submit->enabled);
echo "OK mediator\n";
