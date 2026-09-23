#!/usr/bin/env python3
"""Template health check. Run before sharing the template with anyone.

Checks:
  1. Every referenced vault-relative file path actually exists.
  2. Every skill directory holds a SKILL.md with exactly `name` + `description`.
  3. The skill `name:` matches its directory name.
  4. No stale references to the pre-AGENTS.md layout.

Exit 0 = clean, 1 = findings.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Prefixes for paths created at runtime, not shipped in the template.
RUNTIME_PREFIXES = (
    "sources/greenhouse/",
    "outputs/cron-",
)

STALE = [
    (r"CLAUDE-(recruiter|hrbp|comp|generic)\.md", "role variants now live in roles/"),
    (r"skills/[a-z0-9-]+\.md\b", "skills are now skills/<name>/SKILL.md"),
    (r"user_invocable:", "non-standard skill frontmatter field"),
    (r"^trigger:", "non-standard skill frontmatter field"),
]

PATH_RE = re.compile(r"`([a-z0-9_.\-]+/[a-zA-Z0-9_./\-\[\]]+)`")
FM_RE = re.compile(r"\A---\n(.*?)\n---\n", re.S)


def docs():
    for p in sorted(ROOT.rglob("*.md")):
        if ".git" in p.parts:
            continue
        yield p


def check_paths():
    out = []
    for doc in docs():
        for m in PATH_RE.finditer(doc.read_text(encoding="utf-8")):
            ref = m.group(1)
            if "[" in ref or ref.startswith("~") or ref.startswith(RUNTIME_PREFIXES):
                continue
            if not ref.startswith(("wiki/", "skills/", "sources/", "roles/", "scripts/", "outputs/", "queries/")):
                continue
            target = ROOT / ref
            if not target.exists() and not target.parent.exists():
                out.append(f"{doc.relative_to(ROOT)}: missing path `{ref}`")
    return out


def check_skills():
    out = []
    skills = ROOT / "skills"
    for d in sorted(p for p in skills.iterdir() if p.is_dir()):
        sk = d / "SKILL.md"
        if not sk.exists():
            out.append(f"skills/{d.name}: no SKILL.md")
            continue
        m = FM_RE.match(sk.read_text(encoding="utf-8"))
        if not m:
            out.append(f"skills/{d.name}: no frontmatter")
            continue
        keys = re.findall(r"^([a-z_]+):", m.group(1), re.M)
        extra = [k for k in keys if k not in ("name", "description")]
        if extra:
            out.append(f"skills/{d.name}: non-standard frontmatter {extra}")
        name = re.search(r"^name:\s*(\S+)", m.group(1), re.M)
        if not name:
            out.append(f"skills/{d.name}: no name field")
        elif name.group(1) != d.name:
            out.append(f"skills/{d.name}: name '{name.group(1)}' != directory")
    for stray in skills.glob("*.md"):
        if stray.name != "README.md":
            out.append(f"skills/{stray.name}: flat skill file, should be {stray.stem}/SKILL.md")
    return out


def check_stale():
    out = []
    self_name = Path(__file__).name
    for doc in docs():
        text = doc.read_text(encoding="utf-8")
        for pattern, why in STALE:
            for m in re.finditer(pattern, text, re.M):
                out.append(f"{doc.relative_to(ROOT)}: stale '{m.group(0)}' — {why}")
    for p in sorted(ROOT.rglob("*.html")):
        if ".git" in p.parts:
            continue
        text = p.read_text(encoding="utf-8")
        for pattern, why in STALE[:2]:
            for m in re.finditer(pattern, text, re.M):
                out.append(f"{p.relative_to(ROOT)}: stale '{m.group(0)}' — {why}")
    return [o for o in out if self_name not in o]


def main():
    findings = []
    for label, fn in (("paths", check_paths), ("skills", check_skills), ("stale", check_stale)):
        f = fn()
        print(f"{label:8s} {'OK' if not f else str(len(f)) + ' finding(s)'}")
        findings += f
    if findings:
        print()
        for f in findings:
            print("  " + f)
        return 1
    print("\ntemplate clean")
    return 0


if __name__ == "__main__":
    sys.exit(main())
