# Swift · 责任链（Chain of Responsibility）

[← Swift 选择指南](README.md) · [Skill 入口](../../SKILL.md) · [可运行源码](../../examples/swift/chain-of-responsibility/main.swift)

**分类：行为型** · **代码目标：Swift 6 语言模式**

> 让请求沿一组处理者传递，由每个处理者决定处理、继续或拒绝。

模式意图基于参考站概念页归纳；工程取舍与示例为本项目新编。 [概念依据](https://refactoringguru.cn/design-patterns/chain-of-responsibility) · [来源边界](../../docs/SOURCES.md)

## 问题与动机

请求需按顺序进行若干校验；把规则写死在一个大函数里很难重新组合与独立验证。

**本例场景：** 以可组合规则验证整数必须为正且低于上限，失败立即短路。

## 适用与避免

**适用：** 处理顺序可配置，并且停止条件、默认结果与传递语义明确。

**避免：** 必须执行的步骤不允许跳过，却使用可能无人处理的隐式链。

## 结构、参与者与协作

下图是角色关系示意，不是要求每种语言建立相同类层次。动态语言的协议角色可由方法约定承担。

```mermaid
flowchart LR
Client --> HandlerA
HandlerA -->|继续或停止| HandlerB
HandlerB -->|继续或停止| HandlerC
```

| GoF 角色 | 本例对应职责（成员拼写以代码为准） |
|---|---|
| Handler | Rule：检查当前请求并委派给 next |
| ConcreteHandler | 不同谓词规则或专用处理者 |
| Client | 构建链并提交教学整数请求 |

1. 约定处理者的结果模型：处理完成、继续还是失败。
2. 以固定或可配置顺序组装链，禁止成环。
3. 让未处理请求得到显式结果，不默默丢弃。

## Swift 实现要点

存储闭包需 @escaping；此同步验证链没有 @Sendable 并发契约。短路与链尾结果显式定义，后续改成 async 时必须重新考虑取消与隔离。

**实现定位：** 可运行的最小教学实现；语言机制与模式意图分别说明。

## 完整示例

以下代码与独立源码文件逐字同步；无需第三方业务依赖。测试只覆盖代码中实际写出的断言。

```swift
import Foundation

func check(_ condition: @autoclosure () -> Bool) {
    precondition(condition(), "check failed")
}
enum DemoError: Error { case invalid(String) }
func expectError(_ action: () throws -> Void) {
    var failed = false
    do { try action() } catch { failed = true }
    check(failed)
}

final class Rule {
    private let accepts: (Int) -> Bool
    private let next: Rule?
    init(_ accepts: @escaping (Int) -> Bool, next: Rule? = nil) { self.accepts = accepts; self.next = next }
    func handle(_ value: Int) -> Bool { accepts(value) && (next?.handle(value) ?? true) }
}

var visits = 0
let chain = Rule({ $0 > 0 }, next: Rule({ n in visits += 1; return n < 10 }))
check(!chain.handle(-1) && visits == 0)
check(chain.handle(5) && visits == 1)
check(!chain.handle(12) && visits == 2)
print("OK chain-of-responsibility")
```

## 运行与验证

从仓库根目录执行（先安装对应工具链）：

```sh
cd examples/swift/chain-of-responsibility
swiftc -swift-version 6 main.swift -o demo
./demo
```

期望标准输出：`OK chain-of-responsibility`。任何内嵌断言失败都应导致非零退出；Python 不要使用 `-O` 禁用断言，Swift 不要使用 `-Ounchecked`。

**当前源码状态：已通过编译/运行与内嵌断言。** [完整验证记录](../../docs/VERIFICATION.md)。源码 SHA-256：`8367a46fea0164a1fb46b74f34f687432b65c6912d2f71810f3b3a25abb1d798`。

## 收益与代价

**收益**

- 发送者与具体处理者解耦。
- 处理步骤可复用、重新排序和单独测试。

**代价**

- 顺序会影响结果，调试需要知道经过哪些节点。
- 传统责任链不保证必有处理者；本例采用短路校验链变体。

## 工程边界与常见错误

生产中记录规则标识与短路原因。安全校验链的顺序不能随意让用户重排；异步中间件还需约定 next 是否只能调用一次。

- 每个节点都无条件执行，仍声称具备短路语义。
- 重复调用 next 或形成循环。
- 拒绝后仍执行后面的副作用。

上述工程要求不是运行一次教学示例便能证明的能力；未特别实现的并发访问、外部 I/O、事务、重试与持久化不在本例保证内。

## 扩展测试建议（不等于已全部实现）

- 合法请求经过所有要求的规则。
- 首条失败规则立即停止。
- 终端成功/无人处理语义明确。

针对你的真实输入补充边界/错误用例，再检查替换实现是否保持契约。必要时加入并发竞争、生命周期释放、深度/内存上限和回归测试；不要把断言通过当成生产就绪认证。

## 与替代模式比较

**[命令](command.md)：** 命令封装一次操作；责任链决定请求经过哪些处理者。

**[装饰](decorator.md)：** 装饰常围绕一次调用叠加行为；链明确控制向后传递与停止。

## 来源与继续阅读

- [模式概念](https://refactoringguru.cn/design-patterns/chain-of-responsibility)
- [Swift 官方协议章节源文](https://raw.githubusercontent.com/swiftlang/swift-book/main/TSPL.docc/LanguageGuide/Protocols.md)
- [Swift 官方 ARC 章节源文](https://raw.githubusercontent.com/swiftlang/swift-book/main/TSPL.docc/LanguageGuide/AutomaticReferenceCounting.md)
- [来源分层、原创范围与未覆盖项](../../docs/SOURCES.md)
