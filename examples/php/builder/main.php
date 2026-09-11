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

final readonly class Report {
    /** @param list<string> $sections */
    public function __construct(public string $title, public array $sections) {}
}
final class ReportBuilder {
    private string $title = '';
    /** @var list<string> */
    private array $sections = [];
    public function title(string $value): self { $this->title = trim($value); return $this; }
    public function section(string $value): self { $this->sections[] = $value; return $this; }
    public function build(): Report {
        if ($this->title === '') { throw new InvalidArgumentException('title required'); }
        return new Report($this->title, $this->sections);
    }
}

$b = new ReportBuilder();
expectError(fn() => $b->build());
$first = $b->title('Design')->section('Intent')->build();
$b->section('Tests');
check($first->sections === ['Intent']);
check(count($b->build()->sections) === 2);
echo "OK builder\n";
