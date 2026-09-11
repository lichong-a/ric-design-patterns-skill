# PHP · 装饰（Decorator）

[← PHP 选择指南](README.md) · [Skill 入口](../../SKILL.md) · [可运行源码](../../examples/php/decorator/main.php)

**分类：结构型** · **代码目标：PHP 8.2+（readonly class）**

> 在保持共同契约的前提下，通过可嵌套包装为单个对象叠加行为。

模式意图基于参考站概念页归纳；工程取舍与示例为本项目新编。 [概念依据](https://refactoringguru.cn/design-patterns/decorator) · [来源边界](../../docs/SOURCES.md)

## 问题与动机

文本输出需要按组合增加前缀与括号；为每个组合建立子类不利于扩展。

**本例场景：** 用前缀和括号包装文本，显式展示不同包装顺序。

## 适用与避免

**适用：** 功能要在运行时按需叠加，包装与被包装对象具有可替换的契约。

**避免：** 只是一次简单函数变换，或包装后已经改变了原接口语义。

## 结构、参与者与协作

下图是角色关系示意，不是要求每种语言建立相同类层次。动态语言的协议角色可由方法约定承担。

```mermaid
flowchart LR
Client --> Outer[外层包装]
Outer --> Inner[内层包装]
Inner --> Component
Outer -.-> Contract[统一组件契约]
Component -.-> Contract
```

| GoF 角色 | 本例对应职责（成员拼写以代码为准） |
|---|---|
| Component | Text：render 操作 |
| ConcreteComponent | PlainText：原始文本 |
| Decorator | PrefixText / BracketText：保存并委派给另一个 Text |

1. 保持组件接口足够小。
2. 包装器接收同一接口对象，并在委派前后加行为。
3. 在组合根显式决定包装顺序，测试顺序敏感的输出。

## PHP 实现要点

通过同一个 Text 接口显式转发，而不是依赖 __call 魔术代理；排列顺序改变输出。PHP attributes 是元数据，不等于 GoF 装饰模式。

**实现定位：** 可运行的最小教学实现；语言机制与模式意图分别说明。

## 完整示例

以下代码与独立源码文件逐字同步；无需第三方业务依赖。测试只覆盖代码中实际写出的断言。

```php
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

interface Text { public function render(): string; }
final class PlainText implements Text { public function render(): string { return 'hi'; } }
final readonly class PrefixText implements Text {
    public function __construct(private Text $inner) {}
    public function render(): string { return '!' . $this->inner->render(); }
}
final readonly class BracketText implements Text {
    public function __construct(private Text $inner) {}
    public function render(): string { return '[' . $this->inner->render() . ']'; }
}

check((new BracketText(new PrefixText(new PlainText())))->render() === '[!hi]');
check((new PrefixText(new BracketText(new PlainText())))->render() === '![hi]');
echo "OK decorator\n";
```

## 运行与验证

从仓库根目录执行（先安装对应工具链）：

```sh
php examples/php/decorator/main.php
```

期望标准输出：`OK decorator`。任何内嵌断言失败都应导致非零退出；Python 不要使用 `-O` 禁用断言，Swift 不要使用 `-Ounchecked`。

**当前源码状态：已通过运行与内嵌断言。** [完整验证记录](../../docs/VERIFICATION.md)。源码 SHA-256：`c81886706307b90956bf1aa6b8922ec11aca9870d731b9e2cc0c15bec5ba91eb`。

## 收益与代价

**收益**

- 组合功能而不是枚举所有继承组合。
- 可对单个对象添加责任，不改变其同类实例。

**代价**

- 包装层多时调试路径较长。
- 顺序、对象身份、资源关闭和错误传播更难追踪。

## 工程边界与常见错误

文件或网络装饰链必须定义关闭/取消向内传播的规则。日志、鉴权、重试等包装的顺序有业务后果，不能只测成功输出。

- 忽略装饰顺序的非交换性。
- 包装器没有完整转发原契约。
- 混淆语言 @decorator 语法与 GoF 对象装饰模式。

上述工程要求不是运行一次教学示例便能证明的能力；未特别实现的并发访问、外部 I/O、事务、重试与持久化不在本例保证内。

## 扩展测试建议（不等于已全部实现）

- 两层包装得到预期结果。
- 交换括号与前缀装饰会得到不同输出。
- 失败与资源关闭按既定方向传播。

针对你的真实输入补充边界/错误用例，再检查替换实现是否保持契约。必要时加入并发竞争、生命周期释放、深度/内存上限和回归测试；不要把断言通过当成生产就绪认证。

## 与替代模式比较

**[代理](proxy.md)：** 装饰侧重添加责任；代理侧重控制对主体的访问，外形可能相似。

**[适配器](adapter.md)：** 装饰保留契约；适配器改变客户端所见契约。

## 来源与继续阅读

- [模式概念](https://refactoringguru.cn/design-patterns/decorator)
- [PHP interfaces](https://www.php.net/manual/en/language.oop5.interfaces.php)
- [PHP cloning](https://www.php.net/manual/en/language.oop5.cloning.php)
- [来源分层、原创范围与未覆盖项](../../docs/SOURCES.md)
