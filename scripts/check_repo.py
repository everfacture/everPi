#!/usr/bin/env python3
"""Repository validation for everPi.

No dependencies, no network. This is the boring gate that stops public-facing
repo rot: broken frontmatter, stale README claims, obvious secrets, and Python
syntax errors.
"""
from __future__ import annotations

import json
import py_compile
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

TOKEN_PATTERNS = {
    "github-token": re.compile(rb"gh[pousr]_[A-Za-z0-9_]{20,}"),
    "openai-style-token": re.compile(rb"sk-[A-Za-z0-9_-]{20,}"),
    "google-api-key": re.compile(rb"AIza[0-9A-Za-z_-]{20,}"),
    "telegram-bot-token": re.compile(rb"\b[0-9]{8,12}:[A-Za-z0-9_-]{30,}\b"),
    "private-key": re.compile(rb"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
}

FORBIDDEN_TRACKED_NAMES = {
    ".env",
    "client_secret.json",
    "token.json",
    "auth.json",
    "google_token.json",
    "google_client_secret.json",
}


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def ok(message: str) -> None:
    print(f"ok: {message}")


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def tracked_files() -> list[Path]:
    proc = subprocess.run(
        ["git", "ls-files"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    return [ROOT / line for line in proc.stdout.splitlines() if line.strip()]


def check_package() -> str:
    pkg = json.loads(read("package.json"))
    for key in ["name", "version", "description", "license", "repository", "pi"]:
        if key not in pkg:
            fail(f"package.json missing {key}")
    if pkg["license"] != "MIT":
        fail("package.json license must be MIT")
    version = pkg["version"]
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        fail(f"package.json version is not semver: {version}")
    if pkg.get("pi", {}).get("skills") != ["skills"]:
        fail("package.json pi.skills must point at ['skills']")
    ok(f"package.json valid ({version})")
    return version


def check_docs(version: str) -> None:
    readme = read("README.md")
    changelog = read("CHANGELOG.md")
    if "LICENSE" not in {p.name for p in ROOT.iterdir()}:
        fail("LICENSE file missing")
    if f"version-{version}" not in readme:
        fail("README version badge does not match package.json")
    for banned in [
        "Original source unattributed",
        "ship small bombs",
        "earendil-works/pi-coding-agent",
        "npm install\n/reload",
    ]:
        if banned in readme:
            fail(f"README still contains stale phrase: {banned}")
    if f"## {version}" not in changelog:
        fail(f"CHANGELOG missing section for {version}")
    ok("README/CHANGELOG public claims valid")


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        fail(f"{path.relative_to(ROOT)} missing frontmatter")
    end = text.find("\n---", 4)
    if end == -1:
        fail(f"{path.relative_to(ROOT)} has unterminated frontmatter")
    raw = text[4:end]
    data: dict[str, str] = {}
    for line in raw.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"\'')
    return data


def check_skills() -> None:
    skills_root = ROOT / "skills"
    if not skills_root.is_dir():
        fail("skills/ directory missing")
    skill_dirs = sorted([p for p in skills_root.iterdir() if p.is_dir()])
    if not skill_dirs:
        fail("no skill directories found")
    for skill_dir in skill_dirs:
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            fail(f"{skill_dir.relative_to(ROOT)} missing SKILL.md")
        data = parse_frontmatter(skill_file)
        if data.get("name") != skill_dir.name:
            fail(
                f"{skill_file.relative_to(ROOT)} name mismatch: "
                f"{data.get('name')!r} != {skill_dir.name!r}"
            )
        if not data.get("description"):
            fail(f"{skill_file.relative_to(ROOT)} missing description")
    ok(f"skill frontmatter valid ({len(skill_dirs)} skills)")


def check_python() -> None:
    py_files = sorted((ROOT / "skills").rglob("*.py")) + sorted((ROOT / "scripts").rglob("*.py"))
    for path in py_files:
        py_compile.compile(str(path), doraise=True)
    ok(f"python syntax valid ({len(py_files)} files)")


def check_svg() -> None:
    ET.parse(ROOT / "assets" / "banner.svg")
    banner = read("assets/banner.svg")
    if "ship small diffs" not in banner:
        fail("banner must use public-safe 'ship small diffs' copy")
    ok("banner.svg valid")


def check_tracked_hygiene() -> None:
    files = tracked_files()
    for path in files:
        if path.name in FORBIDDEN_TRACKED_NAMES:
            fail(f"credential-shaped file is tracked: {path.relative_to(ROOT)}")
        data = path.read_bytes()
        for kind, pattern in TOKEN_PATTERNS.items():
            match = pattern.search(data)
            if match:
                line = data[: match.start()].count(b"\n") + 1
                fail(f"secret pattern {kind} in {path.relative_to(ROOT)}:{line}")
    ok(f"tracked-file hygiene valid ({len(files)} files scanned)")


def main() -> int:
    version = check_package()
    check_docs(version)
    check_skills()
    check_python()
    check_svg()
    check_tracked_hygiene()
    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
