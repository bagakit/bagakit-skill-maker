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

## Workflow

1. Capture concrete triggering and non-triggering examples.
2. Keep SKILL.md concise; move deep material to references.
3. Put deterministic/fragile repeatable steps into scripts.
4. Validate and iterate based on over-trigger/under-trigger behavior.
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

    fm, fm_errors = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
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
        if "SKILL.md" not in include_set:
            errors.append("SKILL_PAYLOAD.json include must contain SKILL.md")
        if "README.md" in include_set:
            errors.append("SKILL_PAYLOAD.json include must not contain README.md")
        for path in include:
            if not (skill_dir / path).exists():
                errors.append(f"payload path missing on disk: {path}")
        for runtime_dir in ("scripts", "references", "agents"):
            exists = (skill_dir / runtime_dir).exists()
            has = runtime_dir in include_set
            if exists and not has:
                warnings.append(f"directory exists but not included in payload: {runtime_dir}")
            if has and not exists:
                errors.append(f"payload includes missing directory: {runtime_dir}")

    skill_text = skill_md.read_text(encoding="utf-8")
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
