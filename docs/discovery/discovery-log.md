# Discovery Log

This log is mandatory evidence for search-first before implementation changes.

## skills

- Source: https://github.com/openai/skills
- Checked: catalog structure and reusable skill patterns for search-first workflows
- Relevance: high, directly related to "search before build" behavior
- Usefulness: high, provides reuse-first framing and fallback rules
- Value: can be reused as companion discovery accelerator rules
- Reference Plan: adapt wording into bagakit-skill-maker hard gate section; keep optional accelerator stance
- Authority: primary
- Authority Rationale: official vendor repository with canonical skill contracts and recent maintenance signal

## 权威资料

- 来源: https://github.com/openai/skills
- 查看内容: 技能目录结构、可复用模式描述、技能说明边界
- 关联度: 高，直接支持可复用 skill 优先策略
- 有用程度: 高，可作为“优先复用而非从零实现”的依据
- 价值: 为 discovery gate 提供权威参考源
- 参考计划: 在 discovery playbook 中作为高优先级来源示例保留
- 权威级别: primary
- 权威依据: 官方组织维护的技能仓库，可作为一手规范来源

## 论文

- Source: https://arxiv.org/abs/2406.14545
- Checked: abstract and method framing on retrieval and evidence-grounded decisioning
- Relevance: medium, supports evidence-first design rationale
- Usefulness: medium, helps justify structured evidence logging for decision traceability
- Value: provides methodological backing for explicit discovery evidence fields
- Reference Plan: cite as rationale class; do not hard-code paper-specific process
- Authority: secondary
- Authority Rationale: peer-reviewed research gives strong method rationale but is not runtime contract source

## 开源库

- 来源: https://github.com/anthropics/skills
- 查看内容: skill scaffolding patterns and operational examples
- 关联度: 高，直接可比对跨 agent 技能结构
- 有用程度: 高，可提炼模板和目录组织方式
- 价值: 对 tpl 设计和目录落盘有直接工程价值
- 参考计划: 参考其结构化模板思想，输出到 `docs/discovery/discovery-log-tpl.md`
- 权威级别: primary
- 权威依据: 官方组织维护仓库，文档与样例可作为主仓库级一手资料
