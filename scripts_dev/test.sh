#!/usr/bin/env bash
set -euo pipefail

dev_script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
skill_root="$(cd "${dev_script_dir}/.." && pwd)"
runtime_scripts_dir="${skill_root}/scripts"

tmp="$(mktemp -d -t bagakit-skill-maker-test.XXXXXX)"
trap 'rm -rf "$tmp"' EXIT

echo "[test] compile scripts"
python3 -m py_compile "${runtime_scripts_dir}/bagakit_skill_maker.py"

echo "[test] init"
sh "${runtime_scripts_dir}/bagakit_skill_maker.sh" init --name "Demo Skill" --path "$tmp" --with-agents >/dev/null

target="${tmp}/demo-skill"
[[ -d "$target" ]]
[[ -f "${target}/SKILL.md" ]]
[[ -f "${target}/SKILL_PAYLOAD.json" ]]
[[ -f "${target}/agents/openai.yaml" ]]

echo "[test] payload policy"
python3 - <<PY
import json
from pathlib import Path
p = Path(r"${target}") / "SKILL_PAYLOAD.json"
data = json.loads(p.read_text(encoding="utf-8"))
inc = set(data.get("include", []))
if "README.md" in inc:
    raise SystemExit("README.md must not be in payload include")
for req in ("SKILL.md", "scripts", "references"):
    if req not in inc:
        raise SystemExit(f"missing payload item: {req}")
PY

echo "[test] validate should fail on TODO description"
if sh "${runtime_scripts_dir}/bagakit_skill_maker.sh" validate --skill-dir "$target" >/dev/null 2>&1; then
  echo "[test] expected validate to fail because description still TODO" >&2
  exit 1
fi

echo "[test] fix and validate"
python3 - <<PY
from pathlib import Path
p = Path(r"${target}") / "SKILL.md"
text = p.read_text(encoding="utf-8")
text = text.replace(
    "description: TODO: describe what this skill does and exactly when to use it.",
    "description: Build demo skills from templates when users ask to scaffold and validate skill folders.",
)
p.write_text(text, encoding="utf-8")
PY

sh "${runtime_scripts_dir}/bagakit_skill_maker.sh" validate --skill-dir "$target" >/dev/null

echo "[test] missing when-not-to-use should fail"
python3 - <<PY
from pathlib import Path
import re
p = Path(r"${target}") / "SKILL.md"
text = p.read_text(encoding="utf-8")
text = re.sub(
    r"\n## When NOT to Use This Skill\n(?s:.*?)(?=\n## )",
    "\n",
    text,
    count=1,
)
p.write_text(text, encoding="utf-8")
PY
if sh "${runtime_scripts_dir}/bagakit_skill_maker.sh" validate --skill-dir "$target" >/dev/null 2>&1; then
  echo "[test] expected validation to fail without 'When NOT to Use' section" >&2
  exit 1
fi

echo "[test] restore when-not-to-use section"
python3 - <<PY
from pathlib import Path
p = Path(r"${target}") / "SKILL.md"
text = p.read_text(encoding="utf-8")
insert = """
## When NOT to Use This Skill

- User only needs one-off coding help without reusable skill packaging.
- User asks for mandatory hard-coupling to another skill flow in default mode.

"""
text = text.replace("## Decision Categories\n", insert + "## Decision Categories\n", 1)
p.write_text(text, encoding="utf-8")
PY
sh "${runtime_scripts_dir}/bagakit_skill_maker.sh" validate --skill-dir "$target" >/dev/null

echo "[test] missing fallback path should fail"
python3 - <<PY
from pathlib import Path
import re
p = Path(r"${target}") / "SKILL.md"
text = p.read_text(encoding="utf-8")
text = re.sub(
    r"\n## Fallback Path \\(No Clear Fit\\)\n(?s:.*?)(?=\n## )",
    "\n",
    text,
    count=1,
)
p.write_text(text, encoding="utf-8")
PY
if sh "${runtime_scripts_dir}/bagakit_skill_maker.sh" validate --skill-dir "$target" >/dev/null 2>&1; then
  echo "[test] expected validation to fail without fallback path" >&2
  exit 1
fi

echo "[test] restore fallback path"
python3 - <<PY
from pathlib import Path
p = Path(r"${target}") / "SKILL.md"
text = p.read_text(encoding="utf-8")
insert = """
## Fallback Path (No Clear Skill Fit)

- If boundary is unclear, ask one clarification question about scope/trigger.
- If no reusable pattern is stable, execute task directly and record why no skill route is chosen.

"""
text = text.replace("## Response Templates\n", insert + "## Response Templates\n", 1)
p.write_text(text, encoding="utf-8")
PY
sh "${runtime_scripts_dir}/bagakit_skill_maker.sh" validate --skill-dir "$target" >/dev/null

echo "[test] hard coupling should fail"
python3 - <<PY
from pathlib import Path
p = Path(r"${target}") / "SKILL.md"
text = p.read_text(encoding="utf-8")
text += "\nRun: bash ~/.bagakit/skills/bagakit-long-run/scripts/apply-long-run.sh .\n"
p.write_text(text, encoding="utf-8")
PY
if sh "${runtime_scripts_dir}/bagakit_skill_maker.sh" validate --skill-dir "$target" >/dev/null 2>&1; then
  echo "[test] expected hard coupling validation to fail" >&2
  exit 1
fi

echo "[test] optional contract wording should pass"
python3 - <<PY
from pathlib import Path
p = Path(r"${target}") / "SKILL.md"
text = p.read_text(encoding="utf-8")
text = text.replace(
    "Run: bash ~/.bagakit/skills/bagakit-long-run/scripts/apply-long-run.sh .",
    "Optional contract signal only: if bagakit-long-run is installed, exchange contract schema via docs/.bagakit/inbox/signals.",
)
p.write_text(text, encoding="utf-8")
PY
sh "${runtime_scripts_dir}/bagakit_skill_maker.sh" validate --skill-dir "$target" >/dev/null

echo "[test] pass (${skill_root})"
