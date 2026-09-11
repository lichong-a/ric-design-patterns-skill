# 验证记录

本文件由源码哈希和实际运行记录生成，不凭作者意图把示例标成已通过。

**匹配当前源码且已通过：276/276。** 最后记录时间：`2026-09-11T03:04:06+00:00`。

| 语言 | 通过/示例 | 实测工具链（不是版本推荐） | 环境 |
|---|---:|---|---|
| [Java](../references/java/README.md) | 23/23 | javac 21.0.11; openjdk version "21.0.11" 2026-04-21 | Local / Linux x86_64 |
| [C#](../references/csharp/README.md) | 23/23 | 10.0.400 | GitHub Actions / Linux x86_64 |
| [C++](../references/cpp/README.md) | 23/23 | g++ (Debian 14.2.0-19) 14.2.0 | Local / Linux x86_64 |
| [Go](../references/go/README.md) | 23/23 | go version go1.23.2 linux/amd64 | Local / Linux x86_64 |
| [Rust](../references/rust/README.md) | 23/23 | rustc 1.70.0 (90c541806 2023-05-31) | GitHub Actions / Linux x86_64 |
| [Python](../references/python/README.md) | 23/23 | Python 3.13.5 | Local / Linux x86_64 |
| [TypeScript](../references/typescript/README.md) | 23/23 | Version 5.8.3; v22.16.0 | Local / Linux x86_64 |
| [JavaScript](../references/javascript/README.md) | 23/23 | v22.16.0 | Local / Linux x86_64 |
| [PHP](../references/php/README.md) | 23/23 | PHP 8.4.23 (cli) (built: Jul  3 2026 12:26:56) (NTS) | Local / Linux x86_64 |
| [Ruby](../references/ruby/README.md) | 23/23 | ruby 3.3.8 (2025-04-09 revision b200bad6cd) [x86_64-linux-gnu] | Local / Linux x86_64 |
| [Swift](../references/swift/README.md) | 23/23 | Swift version 6.2.1 (swift-6.2.1-RELEASE) | Local / Linux x86_64 |
| [Kotlin](../references/kotlin/README.md) | 23/23 | info: kotlinc-jvm 1.9.0 (JRE 21.0.11+10-1-deb13u2-Debian); openjdk version "21.0.11" 2026-04-21 | Local / Linux x86_64 |

## 可复现

```sh
python3 scripts/build.py
python3 scripts/validate.py
python3 scripts/run_examples.py --languages python --require-runtimes
python3 scripts/build.py
python3 scripts/validate.py
```

多个语言用逗号分隔；不指定语言时检查全部。缺工具链记录为 skipped，不冒充 passed。`--require-runtimes` 让缺失工具链也导致失败。原始证据在 [data/verification.json](../data/verification.json)，逐例记录状态、SHA-256 和诊断信息。

## 验证做了什么

运行器在临时目录编译/执行独立源码，验证退出码和精确输出 `OK <pattern>`。Java 使用 `--release 17`，C++ 使用 `-std=c++17 -Wall -Wextra -pedantic`，TypeScript 使用 strict + ES2022，Swift 使用 `-swift-version 6`。Kotlin 因各示例命名空间独立，可批量编译再分别启动 main。

结构校验检查 23×12 完整覆盖、分类数量、frontmatter、轻量入口、相对链接、嵌入源码与独立文件一致、SVG XML、路由用例及验证哈希。它不是官方宿主的端到端 Skill 认证。

## 验证没有证明什么

内嵌断言是可观察行为的烟雾/契约测试，不是所有边界的穷尽验证、覆盖率报告、形式证明、性能基准或生产安全审计。未普遍执行跨线程压力、事务故障注入、网络 I/O、跨平台矩阵，也未在所有 Skill 宿主中端到端运行。

JavaScript 与 TypeScript 是同源两种语言产物，分别运行不等于两套独立算法实现的交叉证明。代码目标版本与实际验证版本分开列示；不同编译器或较低版本仍须自行验证。
