# Migration From Old Version

Use this guide when upgrading an old skill contract to current first-principles version.

Policy:
- No runtime backward-compatibility shim by default.
- Migration is explicit and executor-owned (Agentic/human performs file/contract updates).
- If temporary shim is unavoidable, it must be explicitly requested and include removal condition.

## Scope

- Source version: `<old-version-id>`
- Target version: `<new-version-id>`
- Impacted files:
  - `SKILL.md`
  - `SKILL_PAYLOAD.json`
  - `playbook/...` (legacy `reference/...` accepted during migration)
  - `docs/discovery/...`
  - `scripts/...`
  - `gate/...`

## Breaking Changes

| Change | Old | New | Migration Action |
| --- | --- | --- | --- |
| Example: output route key | `driver_ftharness` | `driver + driver_meta` | Replace key usage and clean legacy references |

## Migration Steps

1. Read target `SKILL.md` and identify canonical contracts.
2. Diff old vs new contracts and list all breakpoints.
3. Update files/commands directly to target contract (no dual-path runtime logic).
4. Remove legacy fields/paths/scripts after replacement.
5. Run validation and resolve all hard-gate failures.

## Verification

- Required commands:
  - `sh scripts/bagakit-skill-maker.sh validate --skill-dir <skill-dir>`
- Required evidence:
  - updated file list
  - validation output
  - output/archive destination confirmation

## Notes For Agentic Executors

- Do not preserve old behavior unless explicitly required by user scope.
- Prefer one clean target contract over mixed old/new states.
