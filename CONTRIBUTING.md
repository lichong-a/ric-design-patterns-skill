# 贡献指南

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
