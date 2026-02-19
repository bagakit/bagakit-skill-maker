# AGENTS

For this repository:

- Keep the skill standalone-first.
- Keep cross-skill integration optional and rule-driven (schema/fields), never name-bound mandatory flow calls.
- Keep runtime payload strict in `SKILL_PAYLOAD.json`; do not include `README.md`.
- Use `sh scripts/bagakit_skill_maker.sh validate --skill-dir .` before finalizing edits.
