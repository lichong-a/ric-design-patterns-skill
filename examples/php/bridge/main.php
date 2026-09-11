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

interface Channel { public function send(string $value): string; }
final class EmailChannel implements Channel { public function send(string $value): string { return 'email:' . $value; } }
final class SmsChannel implements Channel { public function send(string $value): string { return 'sms:' . $value; } }
class Notice {
    public function __construct(protected Channel $channel) {}
    public function deliver(string $value): string { return $this->channel->send($value); }
}
final class UrgentNotice extends Notice {
    public function deliver(string $value): string { return $this->channel->send('!' . $value); }
}

check((new Notice(new EmailChannel()))->deliver('hi') === 'email:hi');
check((new UrgentNotice(new SmsChannel()))->deliver('hi') === 'sms:!hi');
echo "OK bridge\n";
