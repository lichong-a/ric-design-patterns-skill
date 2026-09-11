# Java · 装饰（Decorator）

[← Java 选择指南](README.md) · [Skill 入口](../../SKILL.md) · [可运行源码](../../examples/java/decorator/Main.java)

**分类：结构型** · **代码目标：Java 17（通过 --release 17 约束）**

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
| Component | Text：read 操作 |
| ConcreteComponent | PlainText：原始文本 |
| Decorator | PrefixText / BracketText：保存并委派给另一个 Text |

1. 保持组件接口足够小。
2. 包装器接收同一接口对象，并在委派前后加行为。
3. 在组合根显式决定包装顺序，测试顺序敏感的输出。

## Java 实现要点

包装器与部件实现同一个小接口；record 适用于只保存委派引用的教学装饰。资源型包装还需一致的 AutoCloseable 责任。

**实现定位：** 可运行的最小教学实现；语言机制与模式意图分别说明。

## 完整示例

以下代码与独立源码文件逐字同步；无需第三方业务依赖。测试只覆盖代码中实际写出的断言。

```java
import java.util.*;
import java.util.function.*;

public final class Main {
    interface Text { String read(); }
    record PlainText(String value) implements Text {
        public String read() { return value; }
    }
    record PrefixText(Text inner) implements Text {
        public String read() { return "!" + inner.read(); }
    }
    record BracketText(Text inner) implements Text {
        public String read() { return "[" + inner.read() + "]"; }
    }

    static void check(boolean condition) {
        if (!condition) throw new AssertionError("contract failed");
    }
    static void expectThrows(Runnable action) {
        boolean failed = false;
        try { action.run(); } catch (RuntimeException ex) { failed = true; }
        check(failed);
    }

    public static void main(String[] args) {
        check(new BracketText(new PrefixText(new PlainText("hi"))).read().equals("[!hi]"));
        check(new PrefixText(new BracketText(new PlainText("hi"))).read().equals("![hi]"));
        System.out.println("OK decorator");
    }
}
```

## 运行与验证

从仓库根目录执行（先安装对应工具链）：

```sh
cd examples/java/decorator
javac --release 17 Main.java
java -ea Main
```

期望标准输出：`OK decorator`。任何内嵌断言失败都应导致非零退出；Python 不要使用 `-O` 禁用断言，Swift 不要使用 `-Ounchecked`。

**当前源码状态：已通过编译/运行与内嵌断言。** [完整验证记录](../../docs/VERIFICATION.md)。源码 SHA-256：`baa421612c400c60ecc3405bc13bfa44f0e4b53dc4d9d3c7965ea2ac87d5e8a4`。

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
- [Java 函数式接口](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/function/package-summary.html)
- [JLS 类初始化](https://docs.oracle.com/javase/specs/jls/se17/html/jls-12.html#jls-12.4.2)
- [来源分层、原创范围与未覆盖项](../../docs/SOURCES.md)
