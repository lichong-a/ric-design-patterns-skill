# TypeScript · 适配器（Adapter）

[← TypeScript 选择指南](README.md) · [Skill 入口](../../SKILL.md) · [可运行源码](../../examples/typescript/adapter/main.ts)

**分类：结构型** · **代码目标：TypeScript 5.x strict / ES2022 / Node.js 18+ 目标**

> 把已有对象的接口与语义转换为客户端要求的契约。

模式意图基于参考站概念页归纳；工程取舍与示例为本项目新编。 [概念依据](https://refactoringguru.cn/design-patterns/adapter) · [来源边界](../../docs/SOURCES.md)

## 问题与动机

旧测量接口返回厘米，新业务使用米；只改方法名会留下单位错误。

**本例场景：** 把遗留的厘米读数适配为业务要求的米。

## 适用与避免

**适用：** 集成遗留代码、第三方 SDK 或不兼容协议，需要做可追踪的边界转换。

**避免：** 新旧接口本已一致；或适配层掩盖了无法保证的语义兼容性。

## 结构、参与者与协作

下图是角色关系示意，不是要求每种语言建立相同类层次。动态语言的协议角色可由方法约定承担。

```mermaid
flowchart LR
Client --> Target[目标契约]
Target --> Adapter
Adapter -->|转换接口和单位| Legacy[旧 API]
```

| GoF 角色 | 本例对应职责（成员拼写以代码为准） |
|---|---|
| Target | Length：以米为单位的接口 |
| Adaptee | LegacyMeter：返回厘米 |
| Adapter | MeterAdapter：持有旧对象并转换单位 |

1. 明确目标接口的单位、错误、空值和调用约束。
2. 用组合包装旧对象，转换参数、结果与必要的错误。
3. 保持业务逻辑在目标契约后，避免泄漏旧 API。

## TypeScript 实现要点

通过组合适配接口与计量单位；结构化类型系统只验证签名，无法仅凭 number 类型发现厘米/米语义错误。

**实现定位：** 可运行的最小教学实现；语言机制与模式意图分别说明。

## 完整示例

以下代码与独立源码文件逐字同步；无需第三方业务依赖。测试只覆盖代码中实际写出的断言。

```typescript
export {};

function check(condition: boolean, message = "contract failed"): void {
  if (!condition) throw new Error(message);
}
function expectThrows(action: () => unknown): void {
  let failed = false;
  try { action(); } catch { failed = true; }
  check(failed, "expected an error");
}

interface Length { meters(): number; }
class LegacyMeter {
  centimeters(): number { return 250; }
}
class MeterAdapter implements Length {
  constructor(private readonly legacy: LegacyMeter) {}
  meters(): number { return this.legacy.centimeters() / 100; }
}

const length: Length = new MeterAdapter(new LegacyMeter());
check(length.meters() === 2.5);
console.log("OK adapter");
```

## 运行与验证

从仓库根目录执行（先安装对应工具链）：

```sh
cd examples/typescript/adapter
tsc --strict --target ES2022 --module ES2022 main.ts --outDir .build
node --input-type=module < .build/main.js
```

期望标准输出：`OK adapter`。任何内嵌断言失败都应导致非零退出；Python 不要使用 `-O` 禁用断言，Swift 不要使用 `-Ounchecked`。

**当前源码状态：已通过编译/运行与内嵌断言。** [完整验证记录](../../docs/VERIFICATION.md)。源码 SHA-256：`275a36e40cc5520d5fd7bf83e43713b693e3e08dcdf9bb25242ad531eceb9abc`。

## 收益与代价

**收益**

- 让遗留对象可用而不侵入修改。
- 转换逻辑有集中边界，易于契约测试。

**代价**

- 新增一次间接调用与翻译层。
- 错误的语义转换会制造表面兼容。

## 工程边界与常见错误

适配层要记录单位、编码、时区等转换。异步转同步可能阻塞；同步包装并不自动获得超时、取消或重试语义。

- 只改签名，不转换单位或异常语义。
- 把所有下游异常都静默吞掉。
- 继承不必要的复杂类，耦合其内部实现。

上述工程要求不是运行一次教学示例便能证明的能力；未特别实现的并发访问、外部 I/O、事务、重试与持久化不在本例保证内。

## 扩展测试建议（不等于已全部实现）

- 250 厘米转换为 2.5 米。
- 零值和合法边界保持正确单位。
- 按目标契约测试旧接口失败的映射。

针对你的真实输入补充边界/错误用例，再检查替换实现是否保持契约。必要时加入并发竞争、生命周期释放、深度/内存上限和回归测试；不要把断言通过当成生产就绪认证。

## 与替代模式比较

**[外观（门面）](facade.md)：** 适配器处理接口不兼容；外观为复杂子系统提供更简单入口。

**[装饰](decorator.md)：** 装饰保持原契约并叠加行为；适配器转换成另一契约。

## 来源与继续阅读

- [模式概念](https://refactoringguru.cn/design-patterns/adapter)
- [TypeScript classes](https://www.typescriptlang.org/docs/handbook/2/classes.html)
- [JavaScript 迭代协议](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Iteration_protocols)
- [来源分层、原创范围与未覆盖项](../../docs/SOURCES.md)
