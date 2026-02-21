# bagakit-skill-maker

Create and validate portable skills with Bagakit-friendly defaults.

This skill combines:
- official skill-creator scaffolding ideas,
- "The Complete Guide to Building Skills for Claude" design points,
- core portable constraints (standalone-first, optional rule-driven contracts, strict runtime payload),
- optional Bagakit profile guidance.

## What it does

- Scaffold a new skill folder with `SKILL.md`, `SKILL_PAYLOAD.json`, `scripts/`, `references/` (optional `agents/`).
- Validate frontmatter, payload boundaries, and contract policy violations.
- Promote semantic metadata contracts (avoid system-specific key proliferation such as `driver_*`; prefer generic keys like `driver` + `driver_meta`).
- Prefer TOML frontmatter (`+++`) for machine-readable metadata blocks in generated Markdown artifacts.
- Keep a guidance-first constraint budget: gate only hard invariants, avoid over-constraining reasoning with heavy schema.
- Guide keep/split/merge decisions so each skill keeps clear boundaries instead of becoming a toolbox.
- Enforce output-route + archive best practice (deliverable archetype, default route, optional adapters or standalone-only declaration, completion archive gate).
- Provide guidance packs (patterns / anti-patterns / examples) before escalating to heavier gate logic.
- Offer Bagakit ecosystem mappings as optional examples, not hard requirements.
- Support project-local evolution by improving/merging/replacing with upstream best versions under explicit validation.

## Quick Start

```bash
sh scripts/bagakit_skill_maker.sh init --name my-skill --path . --with-agents
sh scripts/bagakit_skill_maker.sh validate --skill-dir ./my-skill
```

## Validation Gates (Final-State)

`validate` enforces:
- trigger-accurate frontmatter (`description` needs explicit "when/适用" semantics),
- semantic metadata contract guidance (avoid one-key-per-adapter schema expansion),
- TOML-first guidance for machine-readable metadata frontmatter in artifacts,
- explicit trigger boundaries in body (`When to Use` / `When NOT to Use`) and fallback path,
- standalone-first design (and `[[BAGAKIT]]` footer when Bagakit profile is enabled),
- cross-skill exchange as optional contract/signal (no hard direct flow call),
- runtime payload hygiene (`README.md` excluded; no duplicate/out-of-root include paths),
- generated docs/runtime files avoid absolute path literals (use relative/env-based paths),
- output archetype clarity (`action-handoff` + `memory-handoff` + archive destination evidence),
- SKILL.md line budget (`<= 500`),
- runtime naming clarity (reject generic/legacy/workaround file names).

## References

- `references/core-design-guide.md` (portable core rules)
- `references/bagakit-profile-guide.md` (Bagakit overlay rules)
- `references/skill-discovery-sources.md` (search-first discovery; standalone with optional ecosystem accelerators)
- `references/guidance-pack-patterns.md`
- `references/guidance-pack-anti-patterns.md`
- `references/guidance-pack-examples.md`
