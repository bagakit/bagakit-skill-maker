---
name: bagakit-skill-maker
description: Create, improve, merge, or refactor Bagakit skills from first principles. Use when you need to scaffold a new skill repo, tighten skill triggers, split SKILL.md into scripts/references for progressive disclosure, convert one or multiple existing skills into a unified Bagakit skill, enforce standalone-first contract rules, or validate SKILL_PAYLOAD/runtime boundaries.
---

# Bagakit Skill Maker

Build skills that are:

- standalone-first,
- rule-driven (not name-bound),
- easy to trigger correctly,
- lean in context cost.

## Granularity Principle (No Toolbox Skill)

- One skill should solve one clearly bounded problem, or one group of problems that share the same foundation.
- Do not build an all-in-one toolbox skill with weak boundaries.
- If boundaries blur, or trigger ambiguity rises, prefer split/merge refactoring:
  - split when one skill contains unrelated workflows,
  - merge when multiple skills duplicate the same foundation and can share one contract.

## Cross-Agent Goal

- Target a portable skill design that works across major coding agents (for example Claude Code, Codex, OpenCode-like runtimes).
- Compatibility should be achieved through generic file contracts, deterministic scripts, and explicit runtime assumptions.
- Never hard-depend on one specific agent surface as a required default path.

## Workflow

1) Lock concrete use cases first.
- Capture 3-5 real user prompts that should trigger the target skill.
- Capture 2-3 neighboring prompts that should NOT trigger it.

2) Design trigger and scope.
- Write a specific `description` in SKILL frontmatter: what it does + when to use.
- Keep one skill focused on one operational job. Split if triggers diverge.
- If user asks to improve one existing skill, keep compatible semantics but remove ambiguity and redundant instructions.
- If user asks to merge multiple skills, combine overlapping workflows into one Bagakit-oriented skill with clear sections and one validation contract.

3) Plan progressive disclosure.
- Keep SKILL.md as an execution map, not a giant handbook.
- Move deep details into `references/`.
- Put deterministic/fragile steps into executable scripts under `scripts/`.

4) Scaffold and edit.
- Run:
```bash
sh scripts/bagakit_skill_maker.sh init --name <skill-name> --path <output-dir> [--with-agents]
```
- Fill generated SKILL.md/references/scripts with project-specific content.

5) Enforce Bagakit constraints.
- Run:
```bash
sh scripts/bagakit_skill_maker.sh validate --skill-dir <skill-dir>
```
- Ensure `SKILL_PAYLOAD.json` excludes `README.md` and only ships runtime payload.
- Ensure cross-skill interaction is optional and schema/rule-driven, never mandatory direct flow-call.

6) Iterate from production misses.
- If over-triggering: narrow frontmatter description with stronger boundaries.
- If under-triggering: add concrete trigger phrases and file/task examples.
- Promote repeated manual fixes into scripts or references.
- If granularity drifts, trigger split/merge with an explicit improve plan + verification matrix.

7) Project-local evolution.
- Bagakit allows project-specific skill recomposition.
- As long as there is a clear improve plan and verifiable checks, the project can evolve its own better skill set.
- Upgrading can be done by merging with the best upstream version (or replacing), then re-validating local trigger quality and contracts.

## Design Guide

- Use one guide file only:
  - `references/design-guide.md`
- Keep all design rules, checklist items, and merge/improve patterns there.

## `[[BAGAKIT]]` Response Driver Technique

- Use **footer driving** instructions to increase task-focused reasoning depth and produce structured observability evidence.
- Keep driving lines as peer lines under one `[[BAGAKIT]]` block (no nested bullets).
- Reuse existing lines from project context (for example `LivingDoc`, `LongRun`), and add new skill-specific lines only when needed.

Minimum pattern:

```text
[[BAGAKIT]]
- LivingDoc: <docs update/evidence>
- LongRun: Item=<id>; Status=<in_progress|done|blocked>; Evidence=<commands/checks>; Next=<resume command>
- SkillMaker: Scope=<create|improve|merge>; Evidence=<trigger tests + payload validation>; Next=<next concrete action>
```

Technique notes:
- `Evidence` must be concrete and executable-oriented (commands, checks, changed contracts), not vague summaries.
- `Next` must be one clear next action, so the next round can continue deterministically.

## Output Contract

When asked to create/refactor a skill, output:
- target folder layout,
- final SKILL frontmatter + core workflow sections,
- runtime payload decision (`SKILL_PAYLOAD.json`),
- granularity decision (keep/split/merge + rationale),
- improve plan and validation matrix,
- validation result with failed/passed checks,
- next iteration suggestions based on trigger quality.

## Non-Goals

- Do not introduce backward-compatibility shims unless explicitly requested.
- Do not hard-bind to one external system name if a rule/schema contract can solve it.
