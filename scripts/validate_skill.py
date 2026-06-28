#!/usr/bin/env python3
"""Validate the superinterview skill contract without external dependencies."""

from __future__ import annotations

import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
KNOWN_PATH_PREFIXES = ("agents/", "docs/", "evals/", "examples/", "reference/", "scripts/", "templates/")
HTML_ARTIFACT_DIRS = ("reference", "templates", "examples")
KNOWN_HTML_ENTITIES = {"amp", "lt", "gt", "quot", "apos", "nbsp", "middot", "rarr"}


class LocalAnchorParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: set[str] = set()
        self.local_hrefs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if values.get("id"):
            self.ids.add(values["id"] or "")
        href = values.get("href")
        if href and href.startswith("#"):
            self.local_hrefs.append(href[1:])


def fail(message: str, failures: list[str]) -> None:
    failures.append(message)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_frontmatter(skill_md: Path, failures: list[str]) -> dict[str, str]:
    text = read_text(skill_md)
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        fail("SKILL.md must start with YAML frontmatter delimited by ---", failures)
        return {}

    frontmatter: dict[str, str] = {}
    for raw_line in match.group(1).splitlines():
        if not raw_line.strip() or raw_line.startswith(" "):
            continue
        if ":" not in raw_line:
            fail(f"Invalid frontmatter line: {raw_line}", failures)
            continue
        key, value = raw_line.split(":", 1)
        frontmatter[key.strip()] = value.strip().strip('"')
    return frontmatter


def validate_frontmatter(failures: list[str]) -> str:
    skill_md = ROOT / "SKILL.md"
    if not skill_md.exists():
        fail("Missing SKILL.md", failures)
        return ""

    frontmatter = parse_frontmatter(skill_md, failures)
    name = frontmatter.get("name", "")
    description = frontmatter.get("description", "")

    if not re.fullmatch(r"[a-z0-9-]{1,64}", name):
        fail("Frontmatter name must be kebab-case and 1-64 characters", failures)
    if not description:
        fail("Frontmatter description is required", failures)
    if len(description) > 1024:
        fail("Frontmatter description must be 1024 characters or fewer", failures)
    if "<" in description or ">" in description:
        fail("Frontmatter description must not contain angle brackets", failures)

    body_lines = read_text(skill_md).split("\n---\n", 1)[-1].splitlines()
    if len(body_lines) > 500:
        fail(f"SKILL.md body should stay under 500 lines; found {len(body_lines)}", failures)

    return name


def validate_reference_links(failures: list[str]) -> None:
    docs = [ROOT / "SKILL.md", ROOT / "README.md"]
    docs += sorted((ROOT / "agents").glob("*.md"))
    docs += sorted((ROOT / "reference").glob("*.md"))

    for doc in docs:
        text = read_text(doc)
        for ref in re.findall(r"`([^`]+)`", text):
            if not ref.startswith(KNOWN_PATH_PREFIXES):
                continue
            ref_path = ROOT / ref
            if not ref_path.exists():
                fail(f"{doc.relative_to(ROOT)} references missing path `{ref}`", failures)


def validate_reveal_contract(failures: list[str]) -> None:
    required = [
        ROOT / "SKILL.md",
        ROOT / "reference" / "mock-loop.md",
        ROOT / "agents" / "critic.md",
    ]
    for path in required:
        text = read_text(path)
        if "reference/system-design-model-answer.html" not in text:
            fail(f"{path.relative_to(ROOT)} must route SYSTEM-DESIGN reveal to the HTML model answer", failures)

    critic = read_text(ROOT / "agents" / "critic.md")
    if "reference/system-design-model-answer.md" in critic:
        fail("agents/critic.md must not reveal the Markdown source instead of the HTML model answer", failures)

    rubric = read_text(ROOT / "reference" / "rubrics.md")
    for marker in ("BEHAVIORAL grade", "CODING grade"):
        if marker not in rubric:
            fail(f"reference/rubrics.md is missing `{marker}` output format", failures)
    if "Real names" in rubric:
        fail("reference/rubrics.md should ask for anonymized behavioral specifics, not real names", failures)


def validate_html_artifacts(failures: list[str]) -> None:
    for folder in HTML_ARTIFACT_DIRS:
        for path in sorted((ROOT / folder).glob("*.html")):
            text = read_text(path)
            rel = path.relative_to(ROOT)
            lower = text.lower()
            for required in ("<!doctype html", "<html", "</html>", "<style", "</style>"):
                if required not in lower:
                    fail(f"{rel} is missing required HTML marker `{required}`", failures)
            if re.search(r"""(?:src|href)=["']https?://""", text):
                fail(f"{rel} should be self-contained and not load external assets", failures)
            visible_markup = re.sub(r"<script\b[^>]*>.*?</script>", "", text, flags=re.DOTALL | re.IGNORECASE)
            visible_markup = re.sub(r"<style\b[^>]*>.*?</style>", "", visible_markup, flags=re.DOTALL | re.IGNORECASE)
            visible_markup = re.sub(r"<!--.*?-->", "", visible_markup, flags=re.DOTALL)
            for line_number, line in enumerate(visible_markup.splitlines(), 1):
                if re.search(r"&(?!#?[A-Za-z0-9]+;)", line):
                    fail(f"{rel}:{line_number} contains an unescaped ampersand", failures)
            for entity in re.findall(r"&([A-Za-z][A-Za-z0-9]+);", visible_markup):
                if entity not in KNOWN_HTML_ENTITIES:
                    fail(f"{rel} contains unknown HTML entity `&{entity};`", failures)

            parser = LocalAnchorParser()
            parser.feed(text)
            for anchor in parser.local_hrefs:
                if anchor and anchor not in parser.ids:
                    fail(f"{rel} links to missing local anchor `#{anchor}`", failures)


def validate_evals(skill_name: str, failures: list[str]) -> None:
    evals_path = ROOT / "evals" / "evals.json"
    if not evals_path.exists():
        fail("Missing evals/evals.json", failures)
        return

    data = json.loads(read_text(evals_path))
    if data.get("skill_name") != skill_name:
        fail("evals/evals.json skill_name must match SKILL.md frontmatter name", failures)

    evals = data.get("evals")
    if not isinstance(evals, list) or len(evals) < 3:
        fail("evals/evals.json should contain at least three realistic eval prompts", failures)
        return

    seen_ids: set[int] = set()
    for item in evals:
        eval_id = item.get("id")
        if not isinstance(eval_id, int) or eval_id in seen_ids:
            fail("Each eval must have a unique integer id", failures)
        seen_ids.add(eval_id)
        if not item.get("prompt") or not item.get("expected_output"):
            fail(f"Eval {eval_id} must include prompt and expected_output", failures)
        if not item.get("expectations"):
            fail(f"Eval {eval_id} should include objective expectations", failures)
        for file_ref in item.get("files", []):
            if not (ROOT / file_ref).exists():
                fail(f"Eval {eval_id} references missing input file `{file_ref}`", failures)


def main() -> int:
    failures: list[str] = []
    skill_name = validate_frontmatter(failures)
    validate_reference_links(failures)
    validate_reveal_contract(failures)
    validate_html_artifacts(failures)
    validate_evals(skill_name, failures)

    if failures:
        print("Validation failed:")
        for item in failures:
            print(f"- {item}")
        return 1

    print("Validation passed: superinterview skill contract is internally consistent.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
