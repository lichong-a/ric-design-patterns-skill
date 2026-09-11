# PHP · 原型（Prototype）

[← PHP 选择指南](README.md) · [Skill 入口](../../SKILL.md) · [可运行源码](../../examples/php/prototype/main.php)

**分类：创建型** · **代码目标：PHP 8.2+（readonly class）**

> 通过已有对象提供的复制能力创建同类对象，而不让客户端依赖其具体构造细节。

模式意图基于参考站概念页归纳；工程取舍与示例为本项目新编。 [概念依据](https://refactoringguru.cn/design-patterns/prototype) · [来源边界](../../docs/SOURCES.md)

## 问题与动机

已有文档模板包含已配置内容，需要派生独立副本；重新拼装既繁琐又可能遗漏字段。

**本例场景：** 复制文档的可变段落容器，再编辑副本验证原对象不受影响。

## 适用与避免

**适用：** 对象配置昂贵、类型运行时确定，或用户从已有模板派生对象。

**避免：** 对象含不可复制资源，或直接构造简单值已足够。

## 结构、参与者与协作

下图是角色关系示意，不是要求每种语言建立相同类层次。动态语言的协议角色可由方法约定承担。

```mermaid
flowchart LR
Client -->|clone / copy| Prototype
Prototype --> Copy[新对象]
Copy -->|独立修改| CopiedState[已复制状态]
```

| GoF 角色 | 本例对应职责（成员拼写以代码为准） |
|---|---|
| Prototype | Document 的 clone / copy 契约 |
| ConcretePrototype | 包含段落列表的文档实现 |
| Client | 从模板得到副本，并独立编辑 |

1. 明确哪些状态独立复制、哪些不可变数据允许共享。
2. 让原型对象或语言复制机制负责复制，而非让外部逐字段猜测。
3. 用可变子对象测试副本隔离；需要图结构时处理环和共享关系。

## PHP 实现要点

PHP clone 默认浅复制属性，__clone 显式复制嵌套 Paragraph 对象。数组值的写时复制不会自动克隆数组里的对象句柄。

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

final class Paragraph {
    public function __construct(public string $text) {}
}
final class Document {
    /** @param list<Paragraph> $paragraphs */
    public function __construct(public string $title, public array $paragraphs) {}
    public function __clone(): void {
        $this->paragraphs = array_map(fn(Paragraph $p): Paragraph => clone $p, $this->paragraphs);
    }
}

$original = new Document('Design', [new Paragraph('one')]);
$copy = clone $original;
$copy->paragraphs[0]->text = 'changed';
$copy->paragraphs[] = new Paragraph('two');
check($original->paragraphs[0]->text === 'one');
check(count($original->paragraphs) === 1 && count($copy->paragraphs) === 2);
echo "OK prototype\n";
```

## 运行与验证

从仓库根目录执行（先安装对应工具链）：

```sh
php examples/php/prototype/main.php
```

期望标准输出：`OK prototype`。任何内嵌断言失败都应导致非零退出；Python 不要使用 `-O` 禁用断言，Swift 不要使用 `-Ounchecked`。

**当前源码状态：已通过运行与内嵌断言。** [完整验证记录](../../docs/VERIFICATION.md)。源码 SHA-256：`61e946b370c7c18672064f687065e483182bd026235262b3563e25d4fc6f6383`。

## 收益与代价

**收益**

- 复用已完成的配置，客户端不依赖具体构造步骤。
- 可用运行时原型注册表替代大量构造分支。

**代价**

- 深复制可能昂贵，且不一定是正确业务语义。
- 句柄、锁、数据库连接、回调与外部身份不能盲目复制。

## 工程边界与常见错误

复制会影响别名与所有权。并发修改中的对象不能在无同步情况下获得一致快照；复制权限凭据或外部资源通常不合理。

- 把赋值当作复制。
- 认为 Clone、record with、data class copy 一定深复制。
- 把 JavaScript 原型链与 GoF 原型模式当作同一概念。

上述工程要求不是运行一次教学示例便能证明的能力；未特别实现的并发访问、外部 I/O、事务、重试与持久化不在本例保证内。

## 扩展测试建议（不等于已全部实现）

- 编辑副本的段落不改变原文档。
- 副本保留其余配置。
- 额外测试环、共享节点和不可复制资源的显式策略。

针对你的真实输入补充边界/错误用例，再检查替换实现是否保持契约。必要时加入并发竞争、生命周期释放、深度/内存上限和回归测试；不要把断言通过当成生产就绪认证。

## 与替代模式比较

**[备忘录](memento.md)：** 原型用于创建另一个对象；备忘录用于恢复同一个对象的历史状态。

**[生成器（建造者）](builder.md)：** 原型从现有状态复制；生成器从步骤构建。

## 来源与继续阅读

- [模式概念](https://refactoringguru.cn/design-patterns/prototype)
- [PHP interfaces](https://www.php.net/manual/en/language.oop5.interfaces.php)
- [PHP cloning](https://www.php.net/manual/en/language.oop5.cloning.php)
- [参考站语言示例抽样](https://refactoringguru.cn/design-patterns/prototype/php/example)
- [来源分层、原创范围与未覆盖项](../../docs/SOURCES.md)
