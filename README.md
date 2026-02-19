# bagakit-skill-maker

Create and validate Bagakit-style skills from first principles.

This skill combines:
- official skill-creator scaffolding ideas,
- "The Complete Guide to Building Skills for Claude" design points,
- Bagakit constraints (standalone-first, optional rule-driven contracts, strict runtime payload).

## What it does

- Scaffold a new skill folder with `SKILL.md`, `SKILL_PAYLOAD.json`, `scripts/`, `references/` (optional `agents/`).
- Validate frontmatter, payload boundaries, and common Bagakit policy violations.
- Guide keep/split/merge decisions so each skill keeps clear boundaries instead of becoming a toolbox.
- Support project-local evolution by improving/merging/replacing with upstream best versions under explicit validation.

## Quick Start

```bash
sh scripts/bagakit_skill_maker.sh init --name my-skill --path /tmp --with-agents
sh scripts/bagakit_skill_maker.sh validate --skill-dir /tmp/my-skill
```

## Validation Gates (Final-State)

`validate` enforces:
- trigger-accurate frontmatter (`description` needs explicit "when/适用" semantics),
- standalone-first design + `[[BAGAKIT]]` footer contract,
- cross-skill exchange as optional contract/signal (no hard direct flow call),
- runtime payload hygiene (`README.md` excluded; no duplicate/out-of-root include paths),
- SKILL.md line budget (`<= 500`),
- runtime naming clarity (reject generic/legacy/workaround file names).

## References

- `references/design-guide.md`
