#!/usr/bin/env python3
"""Deterministically build the skill from reviewed canonical JSON; no network needed."""
from __future__ import annotations
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATEGORIES = {'creational': '创建型', 'structural': '结构型', 'behavioral': '行为型'}

def load(path: str):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))

def write(path: str, content: str) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content.rstrip() + '\n', encoding='utf-8')

def digest(code: str) -> str:
    return hashlib.sha256(code.encode('utf-8')).hexdigest()

def cell(text: str) -> str:
    return text.replace('|', '\\|').replace('\n', ' ')

def bullets(items: list[str]) -> str:
    return '\n'.join('- ' + s for s in items)

GROUPS = [
    ('对象如何产生', ['factory-method', 'abstract-factory', 'builder'], '已有创建者扩展点 → 工厂方法；必须配套的一族产品 → 抽象工厂；分步构建且须校验完整性 → 生成器。', '只有一个稳定构造过程时，用构造函数、具名参数或简单构造函数映射即可。'),
    ('包装一个对象', ['adapter', 'decorator', 'proxy', 'facade'], '接口不兼容 → 适配器；同契约叠加责任 → 装饰；控制访问/按需创建 → 代理；简化多个子系统 → 外观。', '不能只看包装类外形判定；先说明客户端契约是否改变。'),
    ('组织对象结构', ['bridge', 'composite', 'flyweight'], '两个独立变化轴 → 桥接；整体与部分统一处理 → 组合；大量对象重复的不可变状态 → 享元。', '对象少、无内存证据时不要提前引入共享池；平面数据也不必强建对象树。'),
    ('行为怎样变化', ['strategy', 'state', 'template-method'], '客户端选择算法 → 策略；领域事件驱动阶段转换 → 状态；流程骨架固定、局部步骤扩展 → 模板方法。', '少数稳定分支/函数参数往往已足够；三种模式不是消除所有 if 的万能药。'),
    ('请求怎样流转', ['command', 'chain-of-responsibility'], '请求需要保存、排队或撤销 → 命令；请求需经若干处理者择路/短路 → 责任链。', '持久队列、重试、幂等不是模式自动提供的能力；直接调用仍是基线方案。'),
    ('对象怎样协作', ['observer', 'mediator', 'facade'], '一个变化通知多个订阅者 → 观察者；多个同事由中心规则协调 → 中介者；客户端只想更简单入口 → 外观。', '通知与业务决策应分清；简单的一对一调用不用事件总线。'),
    ('怎样访问树与集合', ['iterator', 'visitor', 'interpreter', 'composite'], '只关心遍历 → 迭代器；节点类型稳定且常加操作 → 访问者；为小语法定义求值 → 解释器；树形组织本身 → 组合。', '成熟语言/复杂语法优先专用解析器；封闭小 AST 可以用 enum/模式匹配。'),
    ('复制、历史与撤销', ['prototype', 'memento', 'command'], '创建另一个初始状态相似的对象 → 原型；恢复原对象过去状态 → 备忘录；记录做过的操作与补偿 → 命令。', '先定义深/浅复制、外部资源及历史大小；复制不是撤销，补偿也未必是逆运算。'),
    ('共享实例还是共享数据', ['singleton', 'flyweight'], '特定作用域确需单一实例 → 单例；按键共享多份不同内在状态 → 享元。', '优先比较显式依赖注入与不可变配置；全局访问方便不构成使用单例的充分理由。'),
]

DIAGRAMS = {
'factory-method': 'Client --> Creator\nCreator -->|make| Product\nConcreteCreator -.->|扩展创建步骤| Creator\nConcreteProduct -.->|满足契约| Product',
'abstract-factory': 'Client --> Factory\nFactory --> Button\nFactory --> Checkbox\nLightFactory -.-> Factory\nDarkFactory -.-> Factory',
'builder': 'Client -->|分步配置| Builder\nBuilder -->|校验后 build| Product\nRecipe[可选配方] -.-> Builder',
'prototype': 'Client -->|clone / copy| Prototype\nPrototype --> Copy[新对象]\nCopy -->|独立修改| CopiedState[已复制状态]',
'singleton': 'ClientA --> Access[作用域内统一入口]\nClientB --> Access\nAccess --> Instance[共享实例]',
'adapter': 'Client --> Target[目标契约]\nTarget --> Adapter\nAdapter -->|转换接口和单位| Legacy[旧 API]',
'bridge': 'Notice --> Channel\nUrgentNotice -.-> Notice\nEmail -.-> Channel\nSMS -.-> Channel',
'composite': 'Client --> Item\nBundle -.-> Item\nLeaf -.-> Item\nBundle -->|children| Item',
'decorator': 'Client --> Outer[外层包装]\nOuter --> Inner[内层包装]\nInner --> Component\nOuter -.-> Contract[统一组件契约]\nComponent -.-> Contract',
'facade': 'Client --> Facade\nFacade --> SubsystemA\nFacade --> SubsystemB',
'flyweight': 'ContextA --> Shared[共享内在状态]\nContextB --> Shared\nPool -->|按键创建或复用| Shared',
'proxy': 'Client --> Proxy\nProxy -->|控制访问| RealSubject\nProxy -.-> Contract[共同主体契约]\nRealSubject -.-> Contract',
'chain-of-responsibility': 'Client --> HandlerA\nHandlerA -->|继续或停止| HandlerB\nHandlerB -->|继续或停止| HandlerC',
'command': 'Invoker --> Command\nCommand -->|execute / undo| Receiver\nCommand --> Lifecycle[阶段与必要历史]',
'interpreter': 'Client --> Add\nAdd --> Variable\nAdd --> Literal\nVariable --> Context[变量环境]',
'iterator': 'Client --> IteratorA\nClient --> IteratorB\nIteratorA --> Aggregate\nIteratorB --> Aggregate',
'mediator': 'Toggle -->|事件| Mediator\nMediator -->|协作决策| Button\nMediator -->|拥有或关联| Toggle',
'memento': 'Originator -->|save| Snapshot\nCaretaker -->|保存并交回| Snapshot\nSnapshot -->|restore 与归属检查| Originator',
'observer': 'Subject -->|通知| ListenerA\nSubject -->|通知| ListenerB\nClient -->|注册或退订| Subject',
'state': 'Context --> CurrentState\nLocked -.-> CurrentState\nUnlocked -.-> CurrentState\nLocked -->|coin| Unlocked\nUnlocked -->|enter| Locked',
'strategy': 'Client -->|选择| Context\nContext --> Strategy\nRuleA -.-> Strategy\nRuleB -.-> Strategy',
'template-method': 'Client --> StableFlow[稳定算法骨架]\nStableFlow --> Step[变化步骤]\nConcreteStep -.-> Step',
'visitor': 'Client --> Element\nElement -->|accept| Visitor\nVisitor -->|visitText| TextNode\nVisitor -->|visitNumber| NumberNode',
}

ALIASES = {
'builder':['生成器','建造者','构建器'], 'facade':['外观','门面'],
'chain-of-responsibility':['责任链','职责链'], 'memento':['备忘录','快照恢复'],
'observer':['观察者','订阅通知'], 'state':['状态','状态机'],
'strategy':['策略','算法替换'], 'template-method':['模板方法','流程骨架'],
'visitor':['访问者','双分派'],
}

def role_text(text: str, language: str, slug: str, code: str) -> str:
    replacements = {}
    if language not in ['python','java','typescript','javascript']:
        replacements.update({'Length':'MeterReader','LegacyMeter':'LegacySensor','MeterAdapter':'SensorAdapter','ImageProxy':'LazyImage'})
        if slug == 'decorator': text = text.replace('read 操作','render 操作')
        if slug == 'proxy': text = text.replace('render 操作','read 操作')
    if language == 'csharp':
        replacements.update({s:'I'+s for s in ['Renderer','WidgetFactory','Button','Checkbox','Channel','Item','Text','Image','Expr','Node','NodeVisitor','GateState']})
        replacements['Length']='IMeterReader'
        replacements['MeterReader']='IMeterReader'
    if language == 'go' and slug == 'factory-method':
        replacements['Publisher']='Creator / Publish'
    if language == 'go' and slug == 'template-method':
        replacements['Importer']='Parser / RunImport'
    for before,after in sorted(replacements.items(), key=lambda x: -len(x[0])):
        text = re.sub(r'\b'+re.escape(before)+r'\b',after,text)
    if language in ['javascript','ruby']:
        text += '（未显式声明的接口角色由方法约定承担）'
    return text


def run_command(l: dict, slug: str) -> str:
    path = f"examples/{l['slug']}/{slug}"
    commands = {
        'python':f'python3 {path}/main.py',
        'javascript':f'node {path}/main.mjs',
        'typescript':f'cd {path}\ntsc --strict --target ES2022 --module ES2022 main.ts --outDir .build\nnode --input-type=module < .build/main.js',
        'java':f'cd {path}\njavac --release 17 Main.java\njava -ea Main',
        'cpp':f'cd {path}\ng++ -std=c++17 -Wall -Wextra -pedantic main.cpp -o demo\n./demo',
        'go':f'go run {path}/main.go',
        'rust':f'cd {path}\nrustc --edition=2021 main.rs -o demo\n./demo',
        'php':f'php {path}/main.php',
        'ruby':f'ruby {path}/main.rb',
        'swift':f'cd {path}\nswiftc -swift-version 6 main.swift -o demo\n./demo',
        'kotlin':f'cd {path}\nkotlinc Main.kt -jvm-target 17 -include-runtime -d demo.jar\njava -jar demo.jar',
        'csharp':f'dotnet run --project {path}/Example.csproj --configuration Release',
    }
    return commands[l['slug']]

CSPROJ = '''<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <OutputType>Exe</OutputType>
    <TargetFramework>net8.0</TargetFramework>
    <LangVersion>12.0</LangVersion>
    <Nullable>enable</Nullable>
    <ImplicitUsings>disable</ImplicitUsings>
  </PropertyGroup>
</Project>
'''

def verification_status(records: dict, language: str, slug: str, code: str) -> str:
    record = records.get('languages',{}).get(language,{})
    result = record.get('examples',{}).get(slug,{})
    if result.get('sha256') != digest(code):
        return '待验证（无匹配当前源码哈希的运行记录）'
    if result.get('status') == 'passed':
        return '已通过编译/运行与内嵌断言' if language not in ['python','javascript','php','ruby'] else '已通过运行与内嵌断言'
    return {'failed':'失败：见验证记录','skipped':'未运行：工具链不可用'}.get(result.get('status'),'待验证')


def build() -> None:
    patterns = load('data/patterns.json'); languages = load('data/languages.json')
    release = load('data/release.json'); sources = load('data/sources.json')
    records = load('data/verification.json') if (ROOT/'data/verification.json').exists() else {}
    by_slug = {p['slug']:p for p in patterns}
    banks = {l['slug']:load(f"data/code/{l['slug']}.json") for l in languages}
    def links(slugs, prefix=''):
        return ' / '.join(f"[{by_slug[s]['title']}]({prefix}{s}.md)" for s in slugs)
    route_rows = '\n'.join(f"| {l['name']} | `{l['slug']}` | [选择与目录](references/{l['slug']}/README.md) |" for l in languages)
    skill = f'''---
name: ric-design-patterns-skill
description: 按语言选择、比较、解释和实现 GoF 23 种设计模式。用于设计模式选型、代码重构、模式对比与示例讲解；覆盖 Java、C#、C++、Go、Rust、Python、TypeScript、JavaScript、PHP、Ruby、Swift、Kotlin。先定位真实变化点，再按需读取语言索引与模式详页，避免过度设计。
metadata:
  version: "{release['version']}"
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
{route_rows}

## 输出契约
先给建议与不使用模式的基线，再说明候选差异、选择条件、代价与最小实现。实现时遵循该语言语义，并给出运行命令、关键断言、失败路径与生命周期说明。代码审查先指出实际问题，不为凑模式重构。

## 边界
区分经典结构、语言惯用等价表达与简化变体；Go/Rust 不虚构类继承。解释器为补充项，不在参考站 22 项目录内。示例是教学代码，不自动具备并发、事务、持久化或安全沙箱能力。仅在当前源码有匹配运行记录时称已验证。

可选：`python3 scripts/lookup.py --language <language> --query <pattern>`。只有维护/核验任务才读 [来源](docs/SOURCES.md)、[验证](docs/VERIFICATION.md) 与 [架构](docs/ARCHITECTURE.md)。纯语法、分布式架构或无关任务不要强行套入 GoF。
'''
    write('SKILL.md',skill)
    catalog = {'name':release['name'],'version':release['version'],'counts':{'patterns':len(patterns),'languages':len(languages),'details':len(patterns)*len(languages)},'languages':{},'patterns':{}}
    for p in patterns:
        catalog['patterns'][p['slug']]={'name':p['title'],'english':p['english'],'category':p['category'],'aliases':list(dict.fromkeys([p['title'],p['english'],p['slug']]+ALIASES.get(p['slug'],[])))}
    for l in languages:
        language = l['slug']; bank = banks[language]
        catalog['languages'][language]={'name':l['name'],'aliases':l['aliases'],'index':f'references/{language}/README.md','patterns':{p['slug']:f"references/{language}/{p['slug']}.md" for p in patterns}}
        index = f"# {l['name']} · 设计模式选择指南\n\n[← Skill 入口](../../SKILL.md) · [验证记录](../../docs/VERIFICATION.md)\n\n**代码目标：{l['target']}。** 目标版本不是所有发行版/平台的兼容性承诺，实测版本见验证记录。\n\n"
        index += ('本语言来自用户参考站的语言目录；本项目示例为独立新编。' if l['upstream_index'] else '本语言是额外补充，不声称由用户参考站提供独立语言示例。')+'\n\n## 先看本语言的取舍\n\n'+bullets(l['notes'])+'\n\n'
        for cat,name in CATEGORIES.items():
            index += f'## {name}\n\n| 模式 | 适用信号 | 不使用的基线/警报 | 本语言实现提示 |\n|---|---|---|---|\n'
            for p in patterns:
                if p['category'] != cat: continue
                hint = bank[p['slug']]['idiom'].split('。')[0]+'。'
                index += f"| [{p['title']} · {p['english']}]({p['slug']}.md) | {cell(p['use'])} | {cell(p['avoid'])} | {cell(hint)} |\n"
            index += '\n'
        index += '## 横向选择：先定位变化轴\n\n'
        for title,slugs,decision,baseline in GROUPS:
            index += f'### {title}\n\n{links(slugs)}\n\n{decision}\n\n**先比较更简单方案：** {baseline}\n\n'
        index += '## 阅读与实施顺序\n\n一次只打开最相关的 1–3 个模式详页；明确输入/输出和失败契约后再写实现。示例的内嵌断言与工程测试建议分开：后者不代表已全部执行。\n\n## 来源\n\n'
        index += '\n'.join(f'- [{title}]({url})' for title,url in l['sources'])+'\n'
        if l['upstream_index']: index += f"- [参考站 {l['name']} 目录]({l['upstream_index']})\n"
        if l['sample']: index += f"- [已抽样核对的 {l['sample']} 页面](https://refactoringguru.cn/design-patterns/{l['sample']}/{language}/example)\n"
        write(f'references/{language}/README.md',index)
        for p in patterns:
            slug=p['slug']; example=bank[slug]; code=example['code']
            if not code.endswith('\n'): raise ValueError(f'Canonical source lacks final newline: {language}/{slug}')
            write(f'examples/{language}/{slug}/{l["file"]}',code)
            if language=='csharp': write(f'examples/{language}/{slug}/Example.csproj',CSPROJ)
            status=verification_status(records,language,slug,code)
            roles='\n'.join(f'| {role} | {cell(role_text(text,language,slug,code))} |' for role,text in p['roles'].items())
            special='本页补充 GoF 解释器；用户参考站目录未收录此项。' if slug=='interpreter' else '模式意图基于参考站概念页归纳；工程取舍与示例为本项目新编。'
            page=f'''# {l['name']} · {p['title']}（{p['english']}）

[← {l['name']} 选择指南](README.md) · [Skill 入口](../../SKILL.md) · [可运行源码](../../examples/{language}/{slug}/{l['file']})

**分类：{CATEGORIES[p['category']]}** · **代码目标：{l['target']}**

> {p['intent']}

{special} [概念依据]({p['source']}) · [来源边界](../../docs/SOURCES.md)

## 问题与动机

{p['problem']}

**本例场景：** {p['scenario']}

## 适用与避免

**适用：** {p['use']}

**避免：** {p['avoid']}

## 结构、参与者与协作

下图是角色关系示意，不是要求每种语言建立相同类层次。动态语言的协议角色可由方法约定承担。

```mermaid
flowchart LR
{DIAGRAMS[slug]}
```

| GoF 角色 | 本例对应职责（成员拼写以代码为准） |
|---|---|
{roles}

{chr(10).join(str(i+1)+'. '+s for i,s in enumerate(p['steps']))}

## {l['name']} 实现要点

{example['idiom']}

**实现定位：** {'无类继承语言的意图适配，不伪称经典继承结构。' if language in ['go','rust'] and slug in ['factory-method','template-method'] else '可运行的最小教学实现；语言机制与模式意图分别说明。'}

## 完整示例

以下代码与独立源码文件逐字同步；无需第三方业务依赖。测试只覆盖代码中实际写出的断言。

```{l['fence']}
{code.rstrip()}
```

## 运行与验证

从仓库根目录执行（先安装对应工具链）：

```sh
{run_command(l,slug)}
```

期望标准输出：`OK {slug}`。任何内嵌断言失败都应导致非零退出；Python 不要使用 `-O` 禁用断言，Swift 不要使用 `-Ounchecked`。

**当前源码状态：{status}。** [完整验证记录](../../docs/VERIFICATION.md)。源码 SHA-256：`{digest(code)}`。

## 收益与代价

**收益**

{bullets(p['benefits'])}

**代价**

{bullets(p['costs'])}

## 工程边界与常见错误

{p['engineering']}

{bullets(p['traps'])}

上述工程要求不是运行一次教学示例便能证明的能力；未特别实现的并发访问、外部 I/O、事务、重试与持久化不在本例保证内。

## 扩展测试建议（不等于已全部实现）

{bullets(p['tests'])}

针对你的真实输入补充边界/错误用例，再检查替换实现是否保持契约。必要时加入并发竞争、生命周期释放、深度/内存上限和回归测试；不要把断言通过当成生产就绪认证。

## 与替代模式比较

'''
            for alternative,explanation in p['compare'].items():
                page += f"**[{by_slug[alternative]['title']}]({alternative}.md)：** {explanation}\n\n"
            page += '## 来源与继续阅读\n\n'+f"- [模式概念]({p['source']})\n"+'\n'.join(f'- [{title}]({url})' for title,url in l['sources'])+'\n'
            if l['sample']==slug: page += f'- [参考站语言示例抽样](https://refactoringguru.cn/design-patterns/{slug}/{language}/example)\n'
            page += '- [来源分层、原创范围与未覆盖项](../../docs/SOURCES.md)\n'
            write(f'references/{language}/{slug}.md',page)
    write('catalog.json',json.dumps(catalog,ensure_ascii=False,indent=2))
    build_support_docs(patterns,languages,banks,records,sources,release)
    print(f"Built {len(patterns)*len(languages)} detail pages, {len(languages)} indexes and {len(patterns)*len(languages)} source examples.")


def build_support_docs(patterns,languages,banks,records,sources,release):
    rows=[]; passed=0
    for l in languages:
        language=l['slug']; record=records.get('languages',{}).get(language,{})
        ok=sum(verification_status(records,language,p['slug'],banks[language][p['slug']]['code']).startswith('已通过') for p in patterns)
        passed+=ok
        versions='; '.join(record.get('toolchains',{}).values()) or '尚无运行记录'
        rows.append(f"| [{l['name']}](../references/{language}/README.md) | {ok}/23 | {cell(versions)} | {record.get('environment','未执行')} |")
    verification=f'''# 验证记录

本文件由源码哈希和实际运行记录生成，不凭作者意图把示例标成已通过。

**匹配当前源码且已通过：{passed}/276。** 最后记录时间：`{records.get('updated_at','尚无记录')}`。

| 语言 | 通过/示例 | 实测工具链（不是版本推荐） | 环境 |
|---|---:|---|---|
{chr(10).join(rows)}

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
'''
    write('docs/VERIFICATION.md',verification)
    source_doc=f'''# 来源、范围与内容归属

核验日期：**{sources['accessed_on']}**。共 **{len(sources['sources'])}** 个登记来源。

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

实际核对范围：**{sources['coverage']}**。具体代码页面是抽样，不声称逐行遍历审计原站所有语言的每一份示例。本站最终覆盖矩阵是 **23 模式 × 12 语言 = 276 页/源码**，不是原站页面镜像。

## 需要保留的差异

参考站 Go 工厂方法示例明确采用简单工厂，因为 Go 无类继承；本项目另给“稳定 Publish 工作流 + Creator 接口”的意图适配，并注明它不是经典继承实现。两者不应因同在 factory-method 路径下就被说成完全相同结构。

Rust 的泛型/关联类型与 dyn trait 是不同绑定方案；本项目多数例子选择 dyn 以显示运行时替换，同时说明更轻量替代。Builder 多数为常见单产品验证型变体，Director 为可选；不把任意链式 setter 自动视为完整 GoF 多表示构建。

## 不在范围内

GoF 之外的 MVC、依赖注入、仓储、CQRS、Saga、熔断、分布式一致性和并发模式只可作为边界/替代思路提及；本包没有把它们虚构为第 24 项以后。也没有加入未经测试的语言，只为凑数量复制伪代码。

## 登记来源

'''
    for item in sources['sources']:
        source_doc+=f"### {item['id']} · {item['kind']}\n\n[{item['scope']}]({item['url']})\n\n"
    source_doc+='## 权利说明\n\n本项目没有搬用参考站插图、成段原文或原站代码包；示例为新编教学代码，JavaScript 由本项目 TypeScript 源码去类型生成。来源链接不转移第三方权利，详见 [NOTICE.md](../NOTICE.md)。\n'
    write('docs/SOURCES.md',source_doc)
    write('docs/ARCHITECTURE.md','''# 信息架构与维护约定

```text
ric-design-patterns-skill/
├── SKILL.md                  # 轻量路由，不装入全部知识
├── references/<language>/
│   ├── README.md             # 23 项场景 + 对比选择
│   └── <pattern>.md          # 意图 + 角色 + 示例 + 边界
├── examples/<language>/<pattern>/
│   └── main.* / Main.*       # 与详页逐字同步的可运行代码
├── data/                     # 规范化内容与逐例验证证据
├── scripts/                  # 生成、检索、校验、执行、打包
├── tests/                    # 路由与选型评测样例
├── assets/                   # 原创 SVG，无外部图片依赖
└── docs/                     # 来源、架构、验证说明
```

## 渐进式披露

入口只保留触发条件、语言路由、输出契约与边界。语言已知、模式未知时读取二级页；两者都已知时直接跳到三级页。主入口显式提供第三层路径模板，避免必须沿深链逐页加载。详情自包含概念与源码，不要求再读第四层概念文件。

Agent Skills 规范建议避免深度串联引用；本项目保留用户要求的三层**信息组织**，同时允许直接定位详情，区别于强制三层上下文依赖。来源/验证/维护资料仅维护或核验任务读取。参见 [规范](https://agentskills.io/specification)。

## 单一编辑源

`data/patterns.json` 保存共同概念，`data/languages.json` 保存语言路由与官方资料，`data/code/<language>.json` 保存每个语言的独立代码与特有说明。生成器物化为自包含页面，不在查询时动态拼接，也不要求联网。

修改示例可先编辑独立源码，再用 `scripts/import_example.py` 回填规范源；然后执行测试、生成和结构校验。不要只修改生成页面，否则下一次 build 会覆盖。哈希不一致的旧运行记录会自动降级为待验证。

## 知识维护

新增模式需要更新概念、全部支持语言实现、比较链接与评测用例；GoF 主目录严格保持 23 项，其他模式应新增独立扩展目录而不篡改计数。新增语言需要完整 23 项实现或明确以非完整预览区发布，不把缺页当完成。

`tests/routing-cases.json` 是检索契约测试，`tests/skill-evals.json` 是供真实模型回归使用的判据集合。前者可机械执行，后者未被虚称为已完成的模型基准分数。
''')
    write('NOTICE.md','''# 内容与许可说明

本仓库的中文工程说明、选择表、原创示例、测试和 SVG 由项目新编；JavaScript 示例由同仓 TypeScript 示例编译去类型得到。参考文献仅用于概念与语言语义核验，未将其插图、整页文章或代码包复制进仓库。

第三方名称、商标、文档及链接内容仍归各自权利人所有。来源登记见 docs/SOURCES.md。

本仓库目前尚未选定并附加项目级开源许可证，因此没有展示 MIT/Apache 等授权徽章，也没有把“公开仓库”表述为某种特定许可。后续许可证应由仓库维护者明确选择。
''')
    write('CONTRIBUTING.md','''# 贡献指南

先提交可复现的问题：语言/版本、模式路径、期望行为、实际输出。概念异议请给一手或维护者来源，并区分模式意图与语言实现。

## 修改流程

1. 修改 `data/patterns.json`、`data/languages.json` 或语言源文件。代码可通过下列命令回填，避免手工编辑 JSON 转义：

```sh
python3 scripts/import_example.py --language python --pattern strategy --file examples/python/strategy/main.py
python3 scripts/build.py
python3 scripts/run_examples.py --languages python --require-runtimes
python3 scripts/build.py
python3 scripts/validate.py
```

2. 补充有效/失败路径与真实项目相关边界，检查角色、步骤、运行命令与实际代码一致。
3. 修改来源或新加模式表达时记录依据；不要复制未经许可的插图或教程全文。

## 审查重点

同一模式的跨语言示例要表达同一变化点，但不要求相同类图。函数、协议、trait、enum 和原生迭代器不是“偷工减料”，无依据照搬继承树才是问题。所有“通过”必须有对应源码哈希的实际记录；不承诺未经执行的目标版本兼容。

提交应包含规范源和重新生成的结果。CI 校验/运行的是教学代码，不等于生产安全认证。项目尚未选择开源许可证，许可状态见 NOTICE.md。
''')
    write('.gitignore','''__pycache__/
*.pyc
*.class
*.jar
**/.build/
**/bin/
**/obj/
**/target/
**/demo
*.log
.DS_Store
dist/
''')
    write('docs/CHANGELOG.md',f'''# 更新记录\n\n## {release['version']} · {release['date']}\n\n初始发布：23 种 GoF 模式、12 种语言、276 个自包含详页和独立示例；轻量 Skill 入口、横向选择表、原创 SVG 首页、可复现运行/结构校验/打包工具。明确区分参考站 22 项与补充解释器、10 种参考语言与 2 种补充语言。\n''')
    render_assets()
    language_links=' · '.join(f"[{l['name']}](references/{l['slug']}/README.md)" for l in languages)
    readme=f'''<p align="center">
  <img src="assets/hero.svg" alt="ric-design-patterns-skill：23 种设计模式、12 种语言、按需读取" width="100%" />
</p>

<h1 align="center">ric-design-patterns-skill</h1>
<p align="center"><strong>让模式服务于设计，而不是让设计迁就模式。</strong></p>
<p align="center">GoF 23 · 12 languages · 276 examples · Progressive disclosure</p>
<p align="center">
  <a href="SKILL.md">Skill 入口</a> ·
  <a href="references/typescript/README.md">开始选型</a> ·
  <a href="docs/VERIFICATION.md">验证记录</a> ·
  <a href="docs/SOURCES.md">研究来源</a>
</p>

---

**不只是模式目录，而是一份面向工程决策的 Agent Skill。** 从“哪里会变化”开始，按语言比较候选，再查看可运行实现、适用边界和容易踩的坑。无需把整本模式教材塞进上下文。

| 先选对 | 再写对 | 能核验 |
|---|---|---|
| 每种语言都有 23 项场景与横向对比 | 每个模式都有完整源码、角色映射与运行命令 | 来源分层、源码哈希、编译/运行记录 |
| 总是比较“不用模式”的简单方案 | 不把 Java 类层次硬搬到 Go / Rust | 已验证与待验证明确区分 |

## 三层导航，只读需要的内容

<img src="assets/navigation.svg" alt="SKILL.md 路由到语言选型页，再到语言与模式详页；已知模式可直接跳转" width="100%" />

`SKILL.md` → `references/<language>/README.md` → `references/<language>/<pattern>.md`

已知语言和模式时直接跳转到详情。每个详情自包含：**意图 / 适用与避免 / 结构与角色 / 完整示例 / 代价 / 测试 / 替代方案**。

## 语言入口

{language_links}

**覆盖：** 创建型 5 · 结构型 7 · 行为型 11。参考站的 22 项目录之外，单独补充解释器；JavaScript、Kotlin 为附加语言。范围是 **GoF 23**，不是所有架构、并发与分布式模式的全集。

## 开始使用

```sh
git clone https://github.com/lichong-a/ric-design-patterns-skill.git
```

将整个 `ric-design-patterns-skill` 目录放入你的 Agent Skills 宿主所指定的技能目录，入口为 `SKILL.md`；不同宿主的安装路径/启用方式不同，不只复制入口文件。纯阅读与选型无需安装 12 套工具链，运行某个示例时只需对应语言环境。

把真实约束交给 Agent，而不是只说一个模式名：

> 使用 ric-design-patterns-skill。我的 TypeScript 价格规则需要运行时替换，订单状态又会随事件变化。比较策略、状态和模板方法，先给最简单方案，再给实现与测试。

也可以直接定位：

```sh
python3 scripts/lookup.py --language rust --query "策略"
python3 scripts/run_examples.py --languages python --require-runtimes
```

## 看一眼，再决定是否深入

| 你的问题 | 建议从这里开始 |
|---|---|
| 创建扩展点、产品族与分步构建怎么选？ | [Java 选择指南](references/java/README.md) |
| 回调能否代替一套策略类？ | [TypeScript · 策略](references/typescript/strategy.md) |
| 无继承语言怎样表达稳定流程的创建扩展点？ | [Go · 工厂方法](references/go/factory-method.md) |
| Clone 究竟复制数据还是共享引用？ | [Rust · 原型](references/rust/prototype.md) |
| 包装对象是在加行为，还是控制访问？ | [Python · 装饰](references/python/decorator.md) / [代理](references/python/proxy.md) |

## 质量与边界

当前匹配源码哈希的编译/运行记录：**{passed}/276 通过**。具体版本、未执行项与方法见 [验证记录](docs/VERIFICATION.md)，不是生产就绪或跨平台认证。

示例不搬用上游代码与配图；JavaScript 是本项目 TypeScript 的同源去类型版本。默认教学范围为同步、内存内行为，不自动获得事务、持久化、线程安全或安全沙箱。{len(sources['sources'])} 个登记来源与抽样边界见 [来源说明](docs/SOURCES.md)。

<details>
<summary><strong>维护与复现</strong></summary>

```sh
python3 scripts/build.py
python3 scripts/validate.py
python3 scripts/run_examples.py --languages python --require-runtimes
python3 scripts/build.py
python3 scripts/package.py
```

规范源在 `data/`，页面与独立源码由 `scripts/build.py` 生成；改代码后会以哈希使旧测试记录失效。完整流程见 [贡献指南](CONTRIBUTING.md)。

</details>

---

[信息架构](docs/ARCHITECTURE.md) · [变更记录](docs/CHANGELOG.md) · [贡献指南](CONTRIBUTING.md) · [内容与许可](NOTICE.md)

<sub>为清晰的变化点建立边界，而不是为模式的名字增加类。</sub>
'''
    write('README.md',readme)


def render_assets() -> None:
    write('assets/hero.svg','''<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="460" viewBox="0 0 1280 460" role="img" aria-labelledby="title desc">
<title id="title">ric design patterns skill</title><desc id="desc">Design patterns. Decisions included. 23 patterns, 12 languages and 276 examples in a progressive disclosure skill.</desc>
<defs>
<linearGradient id="bg" x2="1" y2="1"><stop stop-color="#111827"/><stop offset="1" stop-color="#111c2f"/></linearGradient>
<linearGradient id="accent" x2="1" y2="1"><stop stop-color="#83f2cf"/><stop offset="1" stop-color="#77bbef"/></linearGradient>
<pattern id="grid" width="36" height="36" patternUnits="userSpaceOnUse"><path d="M36 0H0V36" fill="none" stroke="#dce6f4" stroke-opacity=".045"/></pattern>
</defs>
<rect width="1280" height="460" rx="24" fill="url(#bg)"/>
<rect width="1280" height="460" rx="24" fill="url(#grid)"/>
<g font-family="Arial, Helvetica, sans-serif">
<rect x="54" y="44" width="44" height="44" rx="12" fill="url(#accent)"/>
<path d="M65 73V58H76M77 73V64H88" fill="none" stroke="#12283a" stroke-width="3" stroke-linecap="round"/>
<text x="112" y="63" fill="#eff5ff" font-size="17" font-weight="700" letter-spacing="1">ric</text>
<text x="112" y="82" fill="#91a4bd" font-size="13" letter-spacing="1.8">DESIGN PATTERNS SKILL</text>
<text x="54" y="169" fill="#f6f8fc" font-size="57" font-weight="700" letter-spacing="-2">Design patterns.</text>
<text x="54" y="234" fill="#a6f1db" font-size="57" font-weight="700" letter-spacing="-2">Decisions included.</text>
<text x="57" y="279" fill="#a6b5ca" font-size="19">Choose the right abstraction. Read only what you need.</text>
<g font-size="14" fill="#d8e2f0">
<rect x="54" y="327" width="145" height="39" rx="19.5" fill="#1c2b40" stroke="#30465d"/>
<text x="76" y="352">23 GoF patterns</text>
<rect x="211" y="327" width="135" height="39" rx="19.5" fill="#1c2b40" stroke="#30465d"/>
<text x="233" y="352">12 languages</text>
<rect x="358" y="327" width="145" height="39" rx="19.5" fill="#1c2b40" stroke="#30465d"/>
<text x="379" y="352">276 examples</text>
</g>
<text x="57" y="414" fill="#69819d" font-size="12" letter-spacing="2.1">INTENT  /  TRADE-OFFS  /  CODE  /  VERIFICATION</text>
<g transform="translate(838 86)">
<rect x="0" y="0" width="310" height="64" rx="12" fill="#20364a" stroke="#76d9c4"/>
<circle cx="29" cy="32" r="6" fill="#a6f1db"/><text x="47" y="38" fill="#e8fff6" font-size="16" font-weight="700">SKILL.md</text>
<text x="270" y="38" fill="#91cdbf" font-size="13">01</text>
<path d="M155 64V96H48V127M155 96H262V127" stroke="#507a8b" stroke-width="2" fill="none"/>
<rect x="-21" y="127" width="138" height="59" rx="10" fill="#1c2b40" stroke="#49647e"/>
<rect x="194" y="127" width="138" height="59" rx="10" fill="#1c2b40" stroke="#49647e"/>
<text x="9" y="163" fill="#d3e2f3" font-size="16">Language</text>
<text x="224" y="163" fill="#d3e2f3" font-size="16">Compare</text>
<path d="M48 186V218H155V245M263 186V218H155" stroke="#507a8b" stroke-width="2" fill="none"/>
<rect x="33" y="245" width="244" height="68" rx="12" fill="#20364a" stroke="#76d9c4"/>
<text x="60" y="273" fill="#a6f1db" font-size="14" font-family="monospace">language / pattern</text>
<text x="60" y="297" fill="#bdccdc" font-size="13">Intent + idiomatic code</text>
</g>
</g></svg>''')
    write('assets/navigation.svg','''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="225" viewBox="0 0 1200 225" role="img" aria-labelledby="title desc">
<title id="title">Three-level navigation</title><desc id="desc">A lightweight skill entry routes to a language selection guide and a self-contained pattern implementation. Known language and pattern can be accessed directly.</desc>
<rect width="1200" height="225" rx="18" fill="#f3f6fa"/>
<g font-family="Arial, Helvetica, sans-serif">
<path d="M330 104H427M762 104H859" stroke="#6f8399" stroke-width="2"/>
<path d="m419 99 8 5-8 5m432-10 8 5-8 5" fill="none" stroke="#6f8399" stroke-width="2"/>
<rect x="30" y="37" width="300" height="130" rx="14" fill="#14253a"/>
<text x="53" y="65" fill="#8fdac7" font-size="11" font-weight="700" letter-spacing="2">01 / ROUTE</text>
<text x="53" y="99" fill="#f5f8fd" font-size="23" font-weight="700">SKILL.md</text>
<text x="53" y="132" fill="#b4c4d8" font-size="15">Language + task + constraints</text>
<rect x="427" y="37" width="335" height="130" rx="14" fill="#fff" stroke="#d4dfe9"/>
<text x="451" y="65" fill="#467d75" font-size="11" font-weight="700" letter-spacing="2">02 / CHOOSE</text>
<text x="451" y="99" fill="#203650" font-size="23" font-weight="700">Language guide</text>
<text x="451" y="132" fill="#60748b" font-size="15">23 use cases + comparisons</text>
<rect x="859" y="37" width="310" height="130" rx="14" fill="#fff" stroke="#98c8ba"/>
<text x="882" y="65" fill="#467d75" font-size="11" font-weight="700" letter-spacing="2">03 / IMPLEMENT</text>
<text x="882" y="99" fill="#203650" font-size="23" font-weight="700">Pattern detail</text>
<text x="882" y="132" fill="#60748b" font-size="15">Code + tests + trade-offs</text>
<text x="600" y="202" text-anchor="middle" fill="#75899d" font-size="12" letter-spacing=".8">KNOWN LANGUAGE + PATTERN? JUMP STRAIGHT TO LEVEL 03.</text>
</g></svg>''')

if __name__ == '__main__':
    build()
