#!/usr/bin/env python3
"""Scaffold and validate Bagakit-style skills."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

NAME_RE = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,62}[a-z0-9])?$")
PLACEHOLDER_HINTS = ("TODO", "[TODO", "replace")
MAX_SKILL_LINES = 500
FILE_STEM_RE = re.compile(r"^[a-z0-9][a-z0-9_-]*$")
GENERIC_FILE_STEMS = {"helper", "helpers", "misc", "tmp", "temp", "util", "utils", "test", "tests"}
LEGACY_TERMS = {"legacy", "compat", "deprecated", "workaround", "shim", "backward", "old"}
OPTIONAL_HINTS = (
    "optional",
    "if available",
    "if installed",
    "contract",
    "schema",
    "signal",
    "可选",
    "契约",
    "信号",
)
ALLOWED_SCRIPT_EXTENSIONS = {".sh", ".py", ".js", ".ts"}
ALLOWED_REFERENCE_EXTENSIONS = {".md", ".txt", ".json", ".yaml", ".yml"}


def eprint(*items: object) -> None:
    print(*items, file=sys.stderr)


def normalize_name(raw: str) -> str:
    name = re.sub(r"[^a-z0-9]+", "-", raw.strip().lower())
    name = re.sub(r"-{2,}", "-", name).strip("-")
    if not name:
        raise SystemExit("error: normalized skill name is empty")
    if not NAME_RE.match(name):
        raise SystemExit(
            "error: invalid skill name after normalization; use lowercase letters, digits, hyphens; max 64 chars"
        )
    return name


def title_case(name: str) -> str:
    return " ".join(part.capitalize() for part in name.split("-"))


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def build_skill_md(name: str) -> str:
    title = title_case(name)
    return f"""---
name: {name}
description: TODO: describe what this skill does and exactly when to use it.
---

# {title}

## Purpose

- Keep this skill focused on one coherent operational job.
- Put "when to use" trigger details in frontmatter `description`.
- Keep the skill standalone-first.

## Workflow

1. Capture concrete triggering and non-triggering examples.
2. Keep SKILL.md concise; move deep material to references.
3. Put deterministic/fragile repeatable steps into scripts.
4. Validate and iterate based on over-trigger/under-trigger behavior.

## Cross-Skill Contract

- Cross-skill interaction must stay optional.
- Exchange only schema/contract signals; never hard-call another skill flow.

## `[[BAGAKIT]]` Footer

```text
[[BAGAKIT]]
- Skill: Status=<in_progress|done|blocked>; Evidence=<checks>; Next=<next action>
```
"""


def build_openai_yaml(name: str) -> str:
    display = title_case(name)
    return (
        "interface:\n"
        f"  display_name: \"{display}\"\n"
        "  short_description: \"TODO: short UI summary\"\n"
        "  default_prompt: \"TODO: one-line default instruction\"\n"
    )


def cmd_init(args: argparse.Namespace) -> int:
    name = normalize_name(args.name)
    root = Path(args.path).expanduser().resolve()
    skill_dir = root / name
    if skill_dir.exists():
        eprint(f"error: target directory already exists: {skill_dir}")
        return 1

    includes = ["SKILL.md", "references", "scripts"]
    if args.with_agents:
        includes.append("agents")

    skill_dir.mkdir(parents=True, exist_ok=False)
    (skill_dir / "references").mkdir(parents=True, exist_ok=True)
    (skill_dir / "scripts").mkdir(parents=True, exist_ok=True)

    write_text(skill_dir / "SKILL.md", build_skill_md(name))
    write_text(
        skill_dir / "SKILL_PAYLOAD.json",
        json.dumps({"version": 1, "include": includes}, indent=2, ensure_ascii=False) + "\n",
    )
    write_text(
        skill_dir / "references" / "start-here.md",
        "# Start Here\n\nAdd reference docs that are too detailed for SKILL.md.\n",
    )

    if args.with_agents:
        write_text(skill_dir / "agents" / "openai.yaml", build_openai_yaml(name))

    print(f"created: {skill_dir}")
    print("next:")
    print(f"  1) edit {skill_dir / 'SKILL.md'}")
    print(f"  2) run: {Path(__file__).name} validate --skill-dir {skill_dir}")
    return 0


def parse_frontmatter(text: str) -> tuple[dict[str, str], list[str]]:
    lines = text.splitlines()
    if len(lines) < 3 or lines[0].strip() != "---":
        return {}, ["SKILL.md must start with YAML frontmatter ('---')"]
    try:
        end = lines.index("---", 1)
    except ValueError:
        return {}, ["SKILL.md frontmatter is not closed with '---'"]

    kv: dict[str, str] = {}
    errors: list[str] = []
    for raw in lines[1:end]:
        line = raw.strip()
        if not line:
            continue
        if ":" not in line:
            errors.append(f"invalid frontmatter line: {raw}")
            continue
        key, value = line.split(":", 1)
        kv[key.strip()] = value.strip().strip('"').strip("'")
    return kv, errors


def load_payload(path: Path) -> tuple[dict[str, Any] | None, list[str]]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None, [f"missing file: {path}"]
    except json.JSONDecodeError as exc:
        return None, [f"invalid json in {path}: {exc}"]
    if not isinstance(data, dict):
        return None, [f"payload root must be object: {path}"]
    return data, []


def line_is_optional_contract(line: str) -> bool:
    lower = line.lower()
    return any(hint in lower for hint in OPTIONAL_HINTS)


def scan_hard_coupling(skill_text: str, own_name: str) -> list[str]:
    errors: list[str] = []
    for idx, line in enumerate(skill_text.splitlines(), 1):
        lower = line.lower()
        for token in re.findall(r"\bbagakit-[a-z0-9-]+\b", lower):
            if token == own_name:
                continue
            if not line_is_optional_contract(lower):
                errors.append(
                    f"line {idx}: cross-skill reference '{token}' must be optional and contract/signal based"
                )

        direct_skill_match = re.search(r"/skills/([a-z0-9-]+)", lower)
        if direct_skill_match and re.search(r"\b(bash|sh|python3?|node)\b", lower):
            target_skill = direct_skill_match.group(1)
            if target_skill != own_name and not line_is_optional_contract(lower):
                errors.append(
                    f"line {idx}: direct call to other skill '{target_skill}' is not allowed without optional contract wording"
                )
    return errors


def audit_runtime_files(skill_dir: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    runtime_dirs = {
        "scripts": ALLOWED_SCRIPT_EXTENSIONS,
        "references": ALLOWED_REFERENCE_EXTENSIONS,
    }

    for dirname, allowed_ext in runtime_dirs.items():
        root = skill_dir / dirname
        if not root.exists():
            continue
        for path in sorted(root.rglob("*")):
            if not path.is_file():
                continue
            rel = path.relative_to(skill_dir)
            stem = path.stem.lower()
            suffix = path.suffix.lower()
            if suffix and suffix not in allowed_ext:
                warnings.append(f"unexpected extension under {dirname}: {rel}")

            if not FILE_STEM_RE.match(stem):
                errors.append(f"file name must be lowercase/digits/hyphen/underscore only: {rel}")

            if stem in GENERIC_FILE_STEMS:
                errors.append(f"file name is too generic (not self-explanatory): {rel}")

            tokens = [tok for tok in re.split(r"[-_]+", stem) if tok]
            bad_terms = sorted(set(tok for tok in tokens if tok in LEGACY_TERMS))
            if bad_terms:
                errors.append(
                    f"file name contains legacy/workaround term {bad_terms}; rewrite to final-state naming: {rel}"
                )

            if "_" in path.name:
                warnings.append(f"prefer hyphen-case file naming for clarity: {rel}")

    return errors, warnings


def cmd_validate(args: argparse.Namespace) -> int:
    skill_dir = Path(args.skill_dir).expanduser().resolve()
    errors: list[str] = []
    warnings: list[str] = []

    skill_md = skill_dir / "SKILL.md"
    payload_file = skill_dir / "SKILL_PAYLOAD.json"
    if not skill_md.exists():
        errors.append(f"missing file: {skill_md}")
    if not payload_file.exists():
        errors.append(f"missing file: {payload_file}")
    if errors:
        for err in errors:
            eprint(f"error: {err}")
        return 1

    skill_text = skill_md.read_text(encoding="utf-8")
    fm, fm_errors = parse_frontmatter(skill_text)
    errors.extend(fm_errors)
    allowed_keys = {"name", "description"}
    unknown = sorted(set(fm.keys()) - allowed_keys)
    if unknown:
        errors.append(f"frontmatter has unsupported keys: {', '.join(unknown)}")

    name = fm.get("name", "")
    description = fm.get("description", "")
    if not name:
        errors.append("frontmatter missing required key: name")
    elif not NAME_RE.match(name):
        errors.append("frontmatter name is invalid; expected lowercase letters/digits/hyphens, max 64 chars")
    if not description:
        errors.append("frontmatter missing required key: description")
    elif any(hint in description for hint in PLACEHOLDER_HINTS):
        errors.append("frontmatter description still looks like placeholder text")
    elif not re.search(r"\bwhen\b|适用|当|用于", description.lower()):
        errors.append("frontmatter description should include clear trigger wording (e.g. 'use when ...')")
    if description and len(description) < 40:
        warnings.append("frontmatter description may be too short for accurate triggering")

    payload, payload_errors = load_payload(payload_file)
    errors.extend(payload_errors)
    include: list[str] = []
    if payload is not None:
        raw_include = payload.get("include")
        if not isinstance(raw_include, list) or not all(isinstance(item, str) for item in raw_include):
            errors.append("SKILL_PAYLOAD.json include must be an array of strings")
        else:
            include = raw_include

    if include:
        include_set = set(include)
        if len(include_set) != len(include):
            errors.append("SKILL_PAYLOAD.json include contains duplicate items")
        if "SKILL.md" not in include_set:
            errors.append("SKILL_PAYLOAD.json include must contain SKILL.md")
        if "README.md" in include_set:
            errors.append("SKILL_PAYLOAD.json include must not contain README.md")
        for path in include:
            if path.startswith("/") or ".." in Path(path).parts:
                errors.append(f"payload path must stay inside skill directory: {path}")
                continue
            if not (skill_dir / path).exists():
                errors.append(f"payload path missing on disk: {path}")
        for runtime_dir in ("scripts", "references", "agents"):
            exists = (skill_dir / runtime_dir).exists()
            has = runtime_dir in include_set
            if exists and not has:
                warnings.append(f"directory exists but not included in payload: {runtime_dir}")
            if has and not exists:
                errors.append(f"payload includes missing directory: {runtime_dir}")

    lines = skill_text.splitlines()
    if len(lines) > MAX_SKILL_LINES:
        errors.append(f"SKILL.md must stay within {MAX_SKILL_LINES} lines (current={len(lines)})")

    if "[[BAGAKIT]]" not in skill_text:
        errors.append("SKILL.md must define [[BAGAKIT]] footer contract")
    if "standalone" not in skill_text.lower():
        errors.append("SKILL.md must state standalone-first design explicitly")
    if not (
        "optional" in skill_text.lower()
        and any(key in skill_text.lower() for key in ("contract", "schema", "signal", "契约", "信号"))
    ):
        errors.append("SKILL.md must describe optional cross-skill contract/signal exchange")
    if "## Workflow" not in skill_text:
        errors.append("SKILL.md must include a '## Workflow' section")

    errors.extend(scan_hard_coupling(skill_text, name or ""))
    runtime_errors, runtime_warnings = audit_runtime_files(skill_dir)
    errors.extend(runtime_errors)
    warnings.extend(runtime_warnings)

    if "bash .bagakit/" in skill_text:
        warnings.append(
            "SKILL.md contains direct '.bagakit' script call; ensure this is optional and not a hard dependency"
        )

    for warning in warnings:
        print(f"warn: {warning}")
    if errors:
        for err in errors:
            eprint(f"error: {err}")
        return 1

    print("ok: skill validation passed")
    if warnings:
        print(f"warn_count={len(warnings)}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Bagakit skill scaffolder and validator")
    sub = parser.add_subparsers(dest="command", required=True)

    p_init = sub.add_parser("init", help="create a new skill skeleton")
    p_init.add_argument("--name", required=True, help="skill name (hyphen-case)")
    p_init.add_argument("--path", default=".", help="parent output directory")
    p_init.add_argument("--with-agents", action="store_true", help="also create agents/openai.yaml")
    p_init.set_defaults(func=cmd_init)

    p_validate = sub.add_parser("validate", help="validate a skill folder")
    p_validate.add_argument("--skill-dir", required=True)
    p_validate.set_defaults(func=cmd_validate)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
