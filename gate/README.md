# Gate Protocol

Use `gate/` as the validation protocol root.

- One subdirectory per validation case (for example `anti-patterns`).
- Each case directory must include:
  - `rules.toml` as the single-source rules file.
  - one or more `check-*.py|sh|js|ts` scripts that read `rules.toml`.
- Keep skill-extension details in `playbook/` (legacy `reference/` accepted); keep process docs in `docs/`; keep validation protocol in `gate/`.
