# Core Design Guide (Portable)

## 1) Target Outcome

Design skills that are:
- standalone-first,
- portable across major coding-agent runtimes,
- not hard-bound to one vendor-specific hook/API,
- deterministic where fragile, flexible where context-dependent.

## 2) Applicability Modes

- **Create**: scaffold a new portable skill from first principles.
- **Improve**: refactor one existing skill to be clearer, leaner, and more trigger-accurate.
- **Merge**: combine multiple skills into one coherent portable skill with unified contract and validation.

## 3) Granularity Rule

- Do not design toolbox skills.
- One skill should own one bounded problem (or one cohesive cluster with the same foundation).
- Split when unrelated foundations are mixed.
- Merge when separate skills duplicate the same foundation.

## 4) Trigger-First Design

Always define:
- 3-5 positive examples (should trigger),
- 2-3 negative examples (must not trigger).

Also require:
- `## When to Use`
- `## When NOT to Use`

## 5) Progressive Disclosure

- Keep `SKILL.md` concise and execution-oriented.
- Put deep material in `references/`.
- Put deterministic repeatable work in `scripts/`.

Rule of thumb:
- high freedom -> text guidance,
- medium freedom -> structured steps/pseudocode,
- low freedom -> executable scripts.

## 6) Core Contract Rules

- Standalone-first execution is mandatory.
- Cross-skill exchange is optional and rule/schema-driven.
- Never require direct flow-calls to another skill as default prerequisite.
- Runtime payload must be explicit in `SKILL_PAYLOAD.json`.
- `README.md` must not be in runtime payload.

## 7) Output + Archive Principle (Completion Gate)

Every skill should define completion using explicit output destinations.

Required:
- Define output set clearly (what files/signals are produced).
- Define default output route when no external driver system is available.
- Define optional adapter routes for external systems (for example task driver, spec system, memory system), or explicitly declare `standalone-only/no-adapter`.
- Define archive gate: each output must have a resolved destination path/id before marking task complete.

Recommended output shape:
- `action-handoff`,
- `memory-handoff`,
- `archive`.

If no driver is detected:
- write a local fallback artifact (for example `plan-<slug>.md`),
- still write archive metadata with destination evidence.

## 8) Deliverable Archetypes

1. **Execution/result-heavy**
- Action: execution completion artifacts.
- Memory: delivery summary/lessons.
- Gate: execution + memory destination both explicit.

2. **Process-driver**
- Action: upstream progression artifacts.
- Memory: route rationale/session summary.
- Gate: upstream target + memory destination explicit.

3. **Memory/governance-heavy**
- Action: governance/docs updates.
- Memory: inbox/memory depositions.
- Gate: docs + memory destinations explicit.

Design requirement:
- If one handoff is intentionally absent, write `none` with rationale.
- Completion is valid only when all required destinations are explicit.

## 9) Improve/Merge Required Outputs

Improve output must include:
- improve plan,
- verification matrix,
- output/archive map,
- deliverable archetype choice + destination rules,
- risk/rollback note.

Merge output must include:
- merge map,
- de-dup rationale,
- output/archive map,
- deliverable archetype choice + destination rules,
- post-merge validation matrix.

## 10) Publish Checklist

- frontmatter valid (`name`, `description` only, no placeholders),
- trigger boundary clear and tested,
- granularity decision explicit and justified,
- payload minimal and runtime-only,
- standalone behavior verified,
- fallback path exists,
- output routes explicit (default + optional adapters),
- archive gate and destination evidence explicit.

## 11) Validator Failure Baseline

Validation should fail on:
- missing trigger semantics in frontmatter (`when/适用/用于`),
- missing standalone-first wording,
- missing `When to Use` / `When NOT to Use`,
- missing fallback path,
- missing output route/default/adapters or archive gate,
- missing action/memory/archive handoff wording,
- hard direct flow-call without optional contract wording,
- payload include drift (duplicate/out-of-root/README),
- oversized `SKILL.md` (`> 500` lines),
- ambiguous legacy/workaround runtime file names.
