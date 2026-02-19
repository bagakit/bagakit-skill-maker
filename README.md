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

## References

- `references/design-guide.md`
