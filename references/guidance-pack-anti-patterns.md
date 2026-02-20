# Guidance Pack: Output/Archive Anti-Patterns

## Anti-Pattern 1: Output Exists, Destination Missing

Symptoms:
- mentions plan/summary/archive
- no concrete destination path/id

Risk:
- completion cannot be audited

Fix:
- add destination evidence fields in output + archive sections.

## Anti-Pattern 2: Adapter-First Without Fallback

Symptoms:
- only external routes described
- local route missing

Risk:
- standalone execution breaks

Fix:
- declare local default route first, adapters second.

## Anti-Pattern 3: Over-Schema For High-Variance Reasoning

Symptoms:
- too many rigid fields for exploratory reasoning
- agent/human adaptation quality drops

Risk:
- workflow becomes compliance-heavy, low-signal

Fix:
- keep guidance pack + examples,
- retain hard gates only for invariants.

## Anti-Pattern 4: Protocol Drift In Footer Blocks

Symptoms:
- `[[BAGAKIT]]` renamed/reformatted
- nested bullets in footer

Risk:
- tools and reviewers lose stable parse target

Fix:
- keep RFDP canonical shape unchanged.

## Anti-Pattern 5: Hard Coupling By Script Invocation

Symptoms:
- required `bash .bagakit/<other-skill>/...` call
- no optional contract wording

Risk:
- hidden dependency across skills

Fix:
- convert to optional contract/signal model + fallback route.
