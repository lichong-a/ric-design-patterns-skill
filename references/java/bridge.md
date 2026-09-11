# Java · 桥接（Bridge）

[← Java 选择指南](README.md) · [Skill 入口](../../SKILL.md) · [可运行源码](../../examples/java/bridge/Main.java)

**分类：结构型** · **代码目标：Java 17（通过 --release 17 约束）**

> 用组合连接抽象与实现，使两个变化维度能够独立扩展。

模式意图基于参考站概念页归纳；工程取舍与示例为本项目新编。 [概念依据](https://refactoringguru.cn/design-patterns/bridge) · [来源边界](../../docs/SOURCES.md)

## 问题与动机

通知有普通与紧急两种形式，发送渠道又有邮件与短信；为每种组合建子类会成倍膨胀。

**本例场景：** 普通或紧急通知可以使用 Email 或 SMS 渠道，展示两个独立维度。

## 适用与避免

**适用：** 产品确实存在两个独立、持续变化的维度，例如消息形式 × 发送渠道。

**避免：** 只有一个变化维度，或所谓第二维只是一个固定实现细节。

## 结构、参与者与协作

下图是角色关系示意，不是要求每种语言建立相同类层次。动态语言的协议角色可由方法约定承担。

```mermaid
flowchart LR
Notice --> Channel
UrgentNotice -.-> Notice
Email -.-> Channel
SMS -.-> Channel
```

| GoF 角色 | 本例对应职责（成员拼写以代码为准） |
|---|---|
| Abstraction | Notice：持有 Channel 并组织消息 |
| RefinedAbstraction | UrgentNotice：改变消息形式 |
| Implementor | Channel：发送接口 |
| ConcreteImplementor | EmailChannel / SmsChannel：渠道实现 |

1. 从变化历史确认两个独立维度。
2. 把底层能力抽为小接口，通过组合注入。
3. 让抽象层在底层能力之上定义自己的业务操作。

## Java 实现要点

抽象层与渠道层分别扩展；组合依赖 final，但渠道内部仍可能可变。实际网络资源应把关闭与异常写进 Channel 契约。

**实现定位：** 可运行的最小教学实现；语言机制与模式意图分别说明。

## 完整示例

以下代码与独立源码文件逐字同步；无需第三方业务依赖。测试只覆盖代码中实际写出的断言。

```java
import java.util.*;
import java.util.function.*;

public final class Main {
    interface Channel { String send(String text); }
    static final class EmailChannel implements Channel {
        public String send(String text) { return "email:" + text; }
    }
    static final class SmsChannel implements Channel {
        public String send(String text) { return "sms:" + text; }
    }
    static class Notice {
        protected final Channel channel;
        Notice(Channel channel) { this.channel = Objects.requireNonNull(channel); }
        String send(String text) { return channel.send(text); }
    }
    static final class UrgentNotice extends Notice {
        UrgentNotice(Channel channel) { super(channel); }
        String send(String text) { return channel.send("!" + text); }
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
        check(new Notice(new EmailChannel()).send("ready").equals("email:ready"));
        check(new Notice(new SmsChannel()).send("ready").equals("sms:ready"));
        check(new UrgentNotice(new EmailChannel()).send("ready").equals("email:!ready"));
        check(new UrgentNotice(new SmsChannel()).send("ready").equals("sms:!ready"));
        System.out.println("OK bridge");
    }
}
```

## 运行与验证

从仓库根目录执行（先安装对应工具链）：

```sh
cd examples/java/bridge
javac --release 17 Main.java
java -ea Main
```

期望标准输出：`OK bridge`。任何内嵌断言失败都应导致非零退出；Python 不要使用 `-O` 禁用断言，Swift 不要使用 `-Ounchecked`。

**当前源码状态：已通过编译/运行与内嵌断言。** [完整验证记录](../../docs/VERIFICATION.md)。源码 SHA-256：`34d113a7a29849b584e9d66068643c4c517f7b92957140e3a73dad90edb59b09`。

## 收益与代价

**收益**

- 避免组合子类数量爆炸。
- 抽象和底层实现可分别测试、演进。

**代价**

- 多一层委派，初期理解成本更高。
- 过早猜测变化维度可能形成无用接口。

## 工程边界与常见错误

实现对象是否拥有连接、是否可以并发共享，需要在 Channel 契约明确。桥接不等于远程透明，网络错误仍应暴露为业务可处理结果。

- 把所有依赖接口的组合都称为桥接，却没有两个可独立扩展的维度。
- 底层接口泄漏具体渠道细节。
- 运行时换渠道时没有定义在途请求归属。

上述工程要求不是运行一次教学示例便能证明的能力；未特别实现的并发访问、外部 I/O、事务、重试与持久化不在本例保证内。

## 扩展测试建议（不等于已全部实现）

- 普通/紧急消息分别组合两种渠道。
- 新增渠道不改消息形式实现。
- 新增消息形式不修改渠道契约。

针对你的真实输入补充边界/错误用例，再检查替换实现是否保持契约。必要时加入并发竞争、生命周期释放、深度/内存上限和回归测试；不要把断言通过当成生产就绪认证。

## 与替代模式比较

**[适配器](adapter.md)：** 桥接是对两个变化维度的组织；适配器通常用于接合已有不兼容接口。

**[策略](strategy.md)：** 策略通常替换一个算法；桥接强调抽象体系与实现体系的独立演进。

## 来源与继续阅读

- [模式概念](https://refactoringguru.cn/design-patterns/bridge)
- [Java 函数式接口](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/function/package-summary.html)
- [JLS 类初始化](https://docs.oracle.com/javase/specs/jls/se17/html/jls-12.html#jls-12.4.2)
- [来源分层、原创范围与未覆盖项](../../docs/SOURCES.md)
