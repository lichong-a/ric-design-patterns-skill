# C++ · 生成器（建造者）（Builder）

[← C++ 选择指南](README.md) · [Skill 入口](../../SKILL.md) · [可运行源码](../../examples/cpp/builder/main.cpp)

**分类：创建型** · **代码目标：C++17**

> 把复杂对象的分步组装与最终表示分开，在完成边界建立对象不变量。

模式意图基于参考站概念页归纳；工程取舍与示例为本项目新编。 [概念依据](https://refactoringguru.cn/design-patterns/builder) · [来源边界](../../docs/SOURCES.md)

## 问题与动机

报告包含标题和多个章节；巨大构造函数难读，直接暴露可变组装过程又会让客户端拿到无效对象。

**本例场景：** 构建带标题和章节列表的报告，在 build 时检查标题非空。

## 适用与避免

**适用：** 有多步骤、可选字段、跨字段校验，或需要用相同组装过程产出不同表示。

**避免：** 少量必填参数可由清晰构造函数、命名参数或不可变记录解决。

## 结构、参与者与协作

下图是角色关系示意，不是要求每种语言建立相同类层次。动态语言的协议角色可由方法约定承担。

```mermaid
flowchart LR
Client -->|分步配置| Builder
Builder -->|校验后 build| Product
Recipe[可选配方] -.-> Builder
```

| GoF 角色 | 本例对应职责（成员拼写以代码为准） |
|---|---|
| Builder | ReportBuilder：积累标题和章节并 build |
| Product | Report：完成后的报告快照 |
| Director | 可选的配方/调用代码：决定组装次序，本例不另设类 |

1. 把构建期状态与最终产品分开。
2. 提供表达领域动作的方法，而不是无约束 setter 集合。
3. 在 build 校验必需状态，再复制或转移所有权形成产品。

## C++ 实现要点

值语义复制 vector 使成品与建造器隔离；仅保证独立快照，不把可修改的 Report 宣称为不可变对象。Director 对此单产品变体非必需。

**实现定位：** 可运行的最小教学实现；语言机制与模式意图分别说明。

## 完整示例

以下代码与独立源码文件逐字同步；无需第三方业务依赖。测试只覆盖代码中实际写出的断言。

```cpp
#include <algorithm>
#include <functional>
#include <iostream>
#include <map>
#include <memory>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>
using std::string;
void check(bool value) { if (!value) throw std::runtime_error("check failed"); }
template<class F> void expect_error(F action) {
    bool failed = false;
    try { action(); } catch (const std::logic_error&) { failed = true; }
    check(failed);
}

struct Report { string title; std::vector<string> sections; };
class ReportBuilder {
    string title_; std::vector<string> sections_;
public:
    ReportBuilder& title(string value) { title_ = std::move(value); return *this; }
    ReportBuilder& section(string value) { sections_.push_back(std::move(value)); return *this; }
    Report build() const {
        if (title_.empty()) throw std::invalid_argument("title required");
        return {title_, sections_};
    }
};

int main() {
    ReportBuilder b;
    expect_error([&]{ b.build(); });
    auto first = b.title("Design").section("Intent").build();
    b.section("Tests");
    check(first.sections.size() == 1 && b.build().sections.size() == 2);
    std::cout << "OK builder\n";
}
```

## 运行与验证

从仓库根目录执行（先安装对应工具链）：

```sh
cd examples/cpp/builder
g++ -std=c++17 -Wall -Wextra -pedantic main.cpp -o demo
./demo
```

期望标准输出：`OK builder`。任何内嵌断言失败都应导致非零退出；Python 不要使用 `-O` 禁用断言，Swift 不要使用 `-Ounchecked`。

**当前源码状态：已通过编译/运行与内嵌断言。** [完整验证记录](../../docs/VERIFICATION.md)。源码 SHA-256：`be4fdc5ab5c048c93c3dcd1772fab983e2b4f38426a3a481285389096408c901`。

## 收益与代价

**收益**

- 把校验收敛到产品形成边界。
- 调用表达意图，可避免组合构造函数膨胀。

**代价**

- 多一个可变组装对象，需要说明是否可复用。
- 链式 API 本身不等于 GoF Builder；本例是现代单产品构建器变体。

## 工程边界与常见错误

默认构建器属于单个请求，不应并发共享。Rust 可消费 self 转移所有权；其他语言要复制可变容器。所谓不可变对象还需检查其成员是否深层可变。

- build 返回内部可变列表，后续操作悄悄修改既有产品。
- 只加 fluent setter，却没有有效性或装配职责。
- 把可选 Director 当成必须存在的空壳类。

上述工程要求不是运行一次教学示例便能证明的能力；未特别实现的并发访问、外部 I/O、事务、重试与持久化不在本例保证内。

## 扩展测试建议（不等于已全部实现）

- 缺少标题时明确失败。
- 完整产品包含预期章节。
- 生成的产品不与构建器意外共享可变章节容器。

针对你的真实输入补充边界/错误用例，再检查替换实现是否保持契约。必要时加入并发竞争、生命周期释放、深度/内存上限和回归测试；不要把断言通过当成生产就绪认证。

## 与替代模式比较

**[抽象工厂](abstract-factory.md)：** 生成器侧重逐步组装；抽象工厂一次选择配套的产品家族。

**[原型](prototype.md)：** 生成器从构建步骤形成新产品；原型从已有状态复制。

## 来源与继续阅读

- [模式概念](https://refactoringguru.cn/design-patterns/builder)
- [C++ Core Guidelines：RAII/所有权](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rr-raii)
- [C++ 工作草案：块作用域声明](https://eel.is/c++draft/stmt.dcl)
- [来源分层、原创范围与未覆盖项](../../docs/SOURCES.md)
