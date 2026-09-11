---
name: ric-design-patterns-skill
description: 按语言选择、比较、解释和实现 GoF 23 种设计模式。用于设计模式选型、代码重构、模式对比与示例讲解；覆盖 Java、C#、C++、Go、Rust、Python、TypeScript、JavaScript、PHP、Ruby、Swift、Kotlin。先定位真实变化点，再按需读取语言索引与模式详页，避免过度设计。
metadata:
  version: "0.1.0"
---
# ric-design-patterns-skill

## 按需读取
1. 从用户任务/仓库确认语言、版本、稳定流程与变化点；信息缺失时陈述假设，不擅自跨语言。
2. 选型不明时只读对应语言索引；已指定模式时可直接读 `references/<language>/<pattern>.md`。
3. 使用下表的 language slug；pattern slug 与路径可在索引或 [catalog.json](catalog.json) 查询。
4. 一般只比较 2–3 个候选，读取 1–3 个详页。**不要预加载全部语言、源码库或参考文献。**

## 语言路由
| 语言 | language slug | 二级页面 |
|---|---|---|
| Java | `java` | [选择与目录](references/java/README.md) |
| C# | `csharp` | [选择与目录](references/csharp/README.md) |
| C++ | `cpp` | [选择与目录](references/cpp/README.md) |
| Go | `go` | [选择与目录](references/go/README.md) |
| Rust | `rust` | [选择与目录](references/rust/README.md) |
| Python | `python` | [选择与目录](references/python/README.md) |
| TypeScript | `typescript` | [选择与目录](references/typescript/README.md) |
| JavaScript | `javascript` | [选择与目录](references/javascript/README.md) |
| PHP | `php` | [选择与目录](references/php/README.md) |
| Ruby | `ruby` | [选择与目录](references/ruby/README.md) |
| Swift | `swift` | [选择与目录](references/swift/README.md) |
| Kotlin | `kotlin` | [选择与目录](references/kotlin/README.md) |

## 输出契约
先给建议与不使用模式的基线，再说明候选差异、选择条件、代价与最小实现。实现时遵循该语言语义，并给出运行命令、关键断言、失败路径与生命周期说明。代码审查先指出实际问题，不为凑模式重构。

## 边界
区分经典结构、语言惯用等价表达与简化变体；Go/Rust 不虚构类继承。解释器为补充项，不在参考站 22 项目录内。示例是教学代码，不自动具备并发、事务、持久化或安全沙箱能力。仅在当前源码有匹配运行记录时称已验证。

可选：`python3 scripts/lookup.py --language <language> --query <pattern>`。只有维护/核验任务才读 [来源](docs/SOURCES.md)、[验证](docs/VERIFICATION.md) 与 [架构](docs/ARCHITECTURE.md)。纯语法、分布式架构或无关任务不要强行套入 GoF。
