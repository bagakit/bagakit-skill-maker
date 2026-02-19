# Skill Design Guide

## 1) Target Outcome

Design skills that are:
- standalone-first,
- portable across major coding-agent runtimes,
- not hard-bound to one vendor-specific hook/API,
- deterministic where fragile, flexible where context-dependent.

## 2) Applicability Modes

This skill supports three modes:
- **Create**: scaffold a new Bagakit skill from first principles.
- **Improve**: refactor one existing skill to be clearer, leaner, and more trigger-accurate.
- **Merge**: combine multiple skills into one coherent Bagakit skill with unified contract and validation.

## 2.1) Granularity Rule (Core)

- Do not design "toolbox" skills.
- A skill should own:
  - one clearly bounded problem, or
  - one cohesive cluster with the same foundational workflow/contract.
- Trigger overlap and conceptual drift are signals to restructure:
  - **Split** when one skill mixes unrelated foundations.
  - **Merge** when multiple skills repeat the same foundation and only differ in thin wrappers.

## 3) Trigger-First Design

Always define:
- 3-5 positive examples (should trigger),
- 2-3 negative examples (must not trigger).

Then refine frontmatter `description` until trigger boundaries are explicit.

## 4) Progressive Disclosure

- Keep `SKILL.md` concise and execution-oriented.
- Put deep material in `references/`.
- Put deterministic repeatable work in `scripts/`.

Rule of thumb:
- high freedom -> text guidance,
- medium freedom -> structured steps/pseudocode,
- low freedom -> executable scripts.

## 5) Bagakit Constraints

- Standalone-first execution is mandatory.
- Cross-skill exchange is optional and rule/schema-driven.
- Never require direct flow-calls to another skill as default prerequisite.
- Runtime payload must be explicit in `SKILL_PAYLOAD.json`.
- `README.md` must not be in runtime payload.

## 6) `[[BAGAKIT]]` Response Driver Technique

Purpose:
- increase focused reasoning for the current task,
- force explicit evidence output,
- improve observability for later review/learning.

Design rules:
- one `[[BAGAKIT]]` footer block,
- peer lines only (no nesting),
- each line includes status + evidence + next action.

Reference pattern:

```text
[[BAGAKIT]]
- LivingDoc: <doc update/evidence>
- LongRun: Item=<id>; Status=<...>; Evidence=<commands/checks>; Next=<resume command>
- SkillMaker: Scope=<create|improve|merge>; Evidence=<trigger tests + payload validation>; Next=<next action>
```

## 7) Improve/Merge Procedure

### Improve one skill
1. Keep intent and trigger domain.
2. Remove ambiguous or duplicated instructions.
3. Move bulky details out of SKILL.md.
4. Add/adjust scripts for deterministic hotspots.
5. Re-validate payload + trigger quality.

Required output:
- improve plan (what changes and why),
- verification matrix (positive/negative triggers + contract checks),
- risk/rollback note.

### Merge multiple skills
1. Map overlapping triggers and workflows.
2. Keep one top-level skill intent; split subflows into sections.
3. Normalize naming, runtime contracts, and output/footer contract.
4. Remove redundant files and compatibility wrappers unless explicitly needed.
5. Validate against positive/negative trigger set.

Required output:
- merge map (source skills -> target sections/contracts),
- de-dup rationale,
- post-merge validation matrix.

## 7.1) Evolution With Upstream Best Version

Bagakit philosophy allows project-local evolution:
- Compare current project skill with best online/upstream version.
- Upgrade via merge (preferred when both have valuable deltas) or replacement (when upstream supersedes local).
- Keep the project's local constraints by re-running contract and trigger validation after upgrade.

## 8) Publish Checklist

- frontmatter valid (`name`, `description` only, no placeholders),
- trigger boundary clear and tested,
- granularity decision is explicit (keep/split/merge) and justified,
- payload minimal and runtime-only,
- standalone behavior works without external skill dependencies,
- optional contract fallback path exists,
- `[[BAGAKIT]]` driver instructions are explicit where the skill needs response-driving behavior.
