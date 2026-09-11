# 来源、范围与内容归属

核验日期：**2026-09-11**。共 **73** 个登记来源。

## 用户给定基础

上传的两份文本只含两个链接：设计模式目录与不同语言示例入口。本项目以这两个链接为起点；没有把不存在的附件研究报告当作已经完成的证据。

参考站目录实际收录 **22** 种模式，语言入口为 **10** 种。GoF 原书出版方目录为 **23** 种；本项目用出版方目录与补充材料加入 **Interpreter（解释器）**。**JavaScript、Kotlin** 是额外语言补充，不伪称参考站提供了这两个独立入口。

## 证据分层

| 层次 | 作用 | 不作出的推断 |
|---|---|---|
| 用户来源/参考站概念页 | 模式术语、三大分类、意图、结构、适用条件 | 不是全部编程语言的规范 |
| GoF 出版方目录 | 校验经典 23 项范围，确认 Interpreter | 不声称已逐页阅读受版权保护的整本书 |
| 语言官方/维护者资料 | 类型、复制、初始化、迭代、所有权与委托等语义 | 不把一个 API 的局部保证扩大到完整程序 |
| 本项目新编内容 | 选型表、工程说明、源码、断言、SVG | 不冒充上游原文或已审计的生产框架 |
| 本地/CI 实际执行 | 当前哈希源码的编译/运行记录 | 不等于全边界、跨平台、并发与安全证明 |

实际核对范围：**22 概念页 + 10 语言目录 + 10 具体代码页面抽样；原书目录与语言文档补充**。具体代码页面是抽样，不声称逐行遍历审计原站所有语言的每一份示例。本站最终覆盖矩阵是 **23 模式 × 12 语言 = 276 页/源码**，不是原站页面镜像。

## 需要保留的差异

参考站 Go 工厂方法示例明确采用简单工厂，因为 Go 无类继承；本项目另给“稳定 Publish 工作流 + Creator 接口”的意图适配，并注明它不是经典继承实现。两者不应因同在 factory-method 路径下就被说成完全相同结构。

Rust 的泛型/关联类型与 dyn trait 是不同绑定方案；本项目多数例子选择 dyn 以显示运行时替换，同时说明更轻量替代。Builder 多数为常见单产品验证型变体，Director 为可选；不把任意链式 setter 自动视为完整 GoF 多表示构建。

## 不在范围内

GoF 之外的 MVC、依赖注入、仓储、CQRS、Saga、熔断、分布式一致性和并发模式只可作为边界/替代思路提及；本包没有把它们虚构为第 24 项以后。也没有加入未经测试的语言，只为凑数量复制伪代码。

## 登记来源

### user-catalog · user-input

[用户上传的目录链接；核验为 22 项目录，不含 Interpreter](https://refactoringguru.cn/design-patterns/catalog)

### user-examples · user-input

[用户上传的示例链接；核验 10 个语言入口](https://refactoringguru.cn/design-patterns/examples)

### gof-publisher · publisher

[GoF 原书的出版方目录：5 创建型、7 结构型、11 行为型，共 23 种](https://www.informit.com/store/design-patterns-elements-of-reusable-object-oriented-9780321770462)

### skill-spec · specification

[frontmatter/目录/渐进式披露；参考建议不等于每个宿主已实测兼容](https://agentskills.io/specification)

### skill-practices · specification

[轻量入口、按需引用、任务导向说明](https://agentskills.io/skill-creation/best-practices)

### pattern-factory-method · concept-page

[意图、结构、适用条件与模式关系；本项目独立组织中文工程说明，不复制原页全文](https://refactoringguru.cn/design-patterns/factory-method)

### pattern-abstract-factory · concept-page

[意图、结构、适用条件与模式关系；本项目独立组织中文工程说明，不复制原页全文](https://refactoringguru.cn/design-patterns/abstract-factory)

### pattern-builder · concept-page

[意图、结构、适用条件与模式关系；本项目独立组织中文工程说明，不复制原页全文](https://refactoringguru.cn/design-patterns/builder)

### pattern-prototype · concept-page

[意图、结构、适用条件与模式关系；本项目独立组织中文工程说明，不复制原页全文](https://refactoringguru.cn/design-patterns/prototype)

### pattern-singleton · concept-page

[意图、结构、适用条件与模式关系；本项目独立组织中文工程说明，不复制原页全文](https://refactoringguru.cn/design-patterns/singleton)

### pattern-adapter · concept-page

[意图、结构、适用条件与模式关系；本项目独立组织中文工程说明，不复制原页全文](https://refactoringguru.cn/design-patterns/adapter)

### pattern-bridge · concept-page

[意图、结构、适用条件与模式关系；本项目独立组织中文工程说明，不复制原页全文](https://refactoringguru.cn/design-patterns/bridge)

### pattern-composite · concept-page

[意图、结构、适用条件与模式关系；本项目独立组织中文工程说明，不复制原页全文](https://refactoringguru.cn/design-patterns/composite)

### pattern-decorator · concept-page

[意图、结构、适用条件与模式关系；本项目独立组织中文工程说明，不复制原页全文](https://refactoringguru.cn/design-patterns/decorator)

### pattern-facade · concept-page

[意图、结构、适用条件与模式关系；本项目独立组织中文工程说明，不复制原页全文](https://refactoringguru.cn/design-patterns/facade)

### pattern-flyweight · concept-page

[意图、结构、适用条件与模式关系；本项目独立组织中文工程说明，不复制原页全文](https://refactoringguru.cn/design-patterns/flyweight)

### pattern-proxy · concept-page

[意图、结构、适用条件与模式关系；本项目独立组织中文工程说明，不复制原页全文](https://refactoringguru.cn/design-patterns/proxy)

### pattern-chain-of-responsibility · concept-page

[意图、结构、适用条件与模式关系；本项目独立组织中文工程说明，不复制原页全文](https://refactoringguru.cn/design-patterns/chain-of-responsibility)

### pattern-command · concept-page

[意图、结构、适用条件与模式关系；本项目独立组织中文工程说明，不复制原页全文](https://refactoringguru.cn/design-patterns/command)

### pattern-interpreter · supplement

[意图、结构、适用条件与模式关系；本项目独立组织中文工程说明，不复制原页全文](https://sourcemaking.com/design_patterns/interpreter)

### pattern-iterator · concept-page

[意图、结构、适用条件与模式关系；本项目独立组织中文工程说明，不复制原页全文](https://refactoringguru.cn/design-patterns/iterator)

### pattern-mediator · concept-page

[意图、结构、适用条件与模式关系；本项目独立组织中文工程说明，不复制原页全文](https://refactoringguru.cn/design-patterns/mediator)

### pattern-memento · concept-page

[意图、结构、适用条件与模式关系；本项目独立组织中文工程说明，不复制原页全文](https://refactoringguru.cn/design-patterns/memento)

### pattern-observer · concept-page

[意图、结构、适用条件与模式关系；本项目独立组织中文工程说明，不复制原页全文](https://refactoringguru.cn/design-patterns/observer)

### pattern-state · concept-page

[意图、结构、适用条件与模式关系；本项目独立组织中文工程说明，不复制原页全文](https://refactoringguru.cn/design-patterns/state)

### pattern-strategy · concept-page

[意图、结构、适用条件与模式关系；本项目独立组织中文工程说明，不复制原页全文](https://refactoringguru.cn/design-patterns/strategy)

### pattern-template-method · concept-page

[意图、结构、适用条件与模式关系；本项目独立组织中文工程说明，不复制原页全文](https://refactoringguru.cn/design-patterns/template-method)

### pattern-visitor · concept-page

[意图、结构、适用条件与模式关系；本项目独立组织中文工程说明，不复制原页全文](https://refactoringguru.cn/design-patterns/visitor)

### index-java · language-index

[已核对语言目录，不表示该语言原站每个具体示例均逐行审计](https://refactoringguru.cn/design-patterns/java)

### sample-java · example-sample

[实际打开的语言示例抽样；本项目代码为独立教学实现，不是复制该页](https://refactoringguru.cn/design-patterns/state/java/example)

### official-java-1 · language-authority

[Java 函数式接口](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/function/package-summary.html)

### official-java-2 · language-authority

[JLS 类初始化](https://docs.oracle.com/javase/specs/jls/se17/html/jls-12.html#jls-12.4.2)

### index-csharp · language-index

[已核对语言目录，不表示该语言原站每个具体示例均逐行审计](https://refactoringguru.cn/design-patterns/csharp)

### sample-csharp · example-sample

[实际打开的语言示例抽样；本项目代码为独立教学实现，不是复制该页](https://refactoringguru.cn/design-patterns/singleton/csharp/example)

### official-csharp-1 · language-authority

[C# 接口](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/types/interfaces)

### official-csharp-2 · language-authority

[Lazy<T>](https://learn.microsoft.com/en-us/dotnet/api/system.lazy-1?view=net-8.0)

### index-cpp · language-index

[已核对语言目录，不表示该语言原站每个具体示例均逐行审计](https://refactoringguru.cn/design-patterns/cpp)

### sample-cpp · example-sample

[实际打开的语言示例抽样；本项目代码为独立教学实现，不是复制该页](https://refactoringguru.cn/design-patterns/visitor/cpp/example)

### official-cpp-1 · language-authority

[C++ Core Guidelines：RAII/所有权](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rr-raii)

### official-cpp-2 · language-authority

[C++ 工作草案：块作用域声明](https://eel.is/c++draft/stmt.dcl)

### index-go · language-index

[已核对语言目录，不表示该语言原站每个具体示例均逐行审计](https://refactoringguru.cn/design-patterns/go)

### sample-go · example-sample

[实际打开的语言示例抽样；本项目代码为独立教学实现，不是复制该页](https://refactoringguru.cn/design-patterns/factory-method/go/example)

### official-go-1 · language-authority

[Effective Go](https://go.dev/doc/effective_go#interfaces_and_types)

### official-go-2 · language-authority

[sync.Once](https://pkg.go.dev/sync#Once)

### official-go-3 · language-authority

[Go 语言规范](https://go.dev/ref/spec)

### index-rust · language-index

[已核对语言目录，不表示该语言原站每个具体示例均逐行审计](https://refactoringguru.cn/design-patterns/rust)

### sample-rust · example-sample

[实际打开的语言示例抽样；本项目代码为独立教学实现，不是复制该页](https://refactoringguru.cn/design-patterns/abstract-factory/rust/example)

### official-rust-1 · language-authority

[Rust Book：trait objects](https://doc.rust-lang.org/book/ch18-02-trait-objects.html)

### official-rust-2 · language-authority

[OnceLock](https://doc.rust-lang.org/std/sync/struct.OnceLock.html)

### index-python · language-index

[已核对语言目录，不表示该语言原站每个具体示例均逐行审计](https://refactoringguru.cn/design-patterns/python)

### sample-python · example-sample

[实际打开的语言示例抽样；本项目代码为独立教学实现，不是复制该页](https://refactoringguru.cn/design-patterns/iterator/python/example)

### official-python-1 · language-authority

[typing.Protocol](https://docs.python.org/3/library/typing.html#typing.Protocol)

### official-python-2 · language-authority

[copy 与 deepcopy](https://docs.python.org/3/library/copy.html)

### index-typescript · language-index

[已核对语言目录，不表示该语言原站每个具体示例均逐行审计](https://refactoringguru.cn/design-patterns/typescript)

### sample-typescript · example-sample

[实际打开的语言示例抽样；本项目代码为独立教学实现，不是复制该页](https://refactoringguru.cn/design-patterns/strategy/typescript/example)

### official-typescript-1 · language-authority

[TypeScript classes](https://www.typescriptlang.org/docs/handbook/2/classes.html)

### official-typescript-2 · language-authority

[JavaScript 迭代协议](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Iteration_protocols)

### official-javascript-1 · language-authority

[ECMAScript 标准入口](https://ecma-international.org/publications-and-standards/standards/ecma-262/)

### index-php · language-index

[已核对语言目录，不表示该语言原站每个具体示例均逐行审计](https://refactoringguru.cn/design-patterns/php)

### sample-php · example-sample

[实际打开的语言示例抽样；本项目代码为独立教学实现，不是复制该页](https://refactoringguru.cn/design-patterns/prototype/php/example)

### official-php-1 · language-authority

[PHP interfaces](https://www.php.net/manual/en/language.oop5.interfaces.php)

### official-php-2 · language-authority

[PHP cloning](https://www.php.net/manual/en/language.oop5.cloning.php)

### index-ruby · language-index

[已核对语言目录，不表示该语言原站每个具体示例均逐行审计](https://refactoringguru.cn/design-patterns/ruby)

### sample-ruby · example-sample

[实际打开的语言示例抽样；本项目代码为独立教学实现，不是复制该页](https://refactoringguru.cn/design-patterns/decorator/ruby/example)

### official-ruby-1 · language-authority

[Ruby Enumerable](https://docs.ruby-lang.org/en/master/Enumerable.html)

### official-ruby-2 · language-authority

[Ruby Singleton](https://docs.ruby-lang.org/en/master/Singleton.html)

### index-swift · language-index

[已核对语言目录，不表示该语言原站每个具体示例均逐行审计](https://refactoringguru.cn/design-patterns/swift)

### sample-swift · example-sample

[实际打开的语言示例抽样；本项目代码为独立教学实现，不是复制该页](https://refactoringguru.cn/design-patterns/mediator/swift/example)

### official-swift-1 · language-authority

[Swift 官方协议章节源文](https://raw.githubusercontent.com/swiftlang/swift-book/main/TSPL.docc/LanguageGuide/Protocols.md)

### official-swift-2 · language-authority

[Swift 官方 ARC 章节源文](https://raw.githubusercontent.com/swiftlang/swift-book/main/TSPL.docc/LanguageGuide/AutomaticReferenceCounting.md)

### official-kotlin-1 · language-authority

[Kotlin delegation](https://kotlinlang.org/docs/delegation.html)

### official-kotlin-2 · language-authority

[Kotlin object declarations](https://kotlinlang.org/docs/object-declarations.html)

### official-kotlin-3 · language-authority

[Kotlin delegated properties / lazy](https://kotlinlang.org/docs/delegated-properties.html)

## 权利说明

本项目没有搬用参考站插图、成段原文或原站代码包；示例为新编教学代码，JavaScript 由本项目 TypeScript 源码去类型生成。来源链接不转移第三方权利，详见 [NOTICE.md](../NOTICE.md)。
