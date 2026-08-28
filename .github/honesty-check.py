#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Checks this repository's own text against the rules it is written under.

Run locally:  python3 .github/honesty-check.py

  1. SCOPE      No claim of a discipline that was not practised. This is an
                automation portfolio; it does not do machine-learning research.
  2. HONESTY    No percentage, multiplier or money figure without a stated
                measurement method on the same line. An unsourced number is
                the fastest way to lose a technical reader.
  3. PROVENANCE The availability disclosure must be present on every
                client-facing page — the README and the standalone demo,
                checked separately, because the demo is one file and may well
                be opened with no README in sight.

Exit code 1 if anything fails.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BANNED = [
    # rule 1 — scope
    (r"\bcomputer vision\b",             "claims a discipline not practised"),
    (r"\bNLP\b",                         "claims a discipline not practised"),
    (r"\bnatural language processing\b", "claims a discipline not practised"),
    (r"\bdeep learning\b",               "claims a discipline not practised"),
    (r"\bneural network\b",              "claims a discipline not practised"),
    (r"\bmachine learning\b",            "claims a discipline not practised"),
    (r"\bML (model|pipeline|engineer)\b", "claims a discipline not practised"),
    (r"\bmodel training\b",              "provider APIs are called, not trained"),
    (r"\bfine-?tun(e|ing|ed)\b",         "provider APIs are called, not tuned"),
    (r"\btrained (a|our|the) model\b",   "provider APIs are called, not trained"),
    (r"\bRAG\b",                         "not built in this system"),
    (r"\bvector (database|store|embedding)\b", "not built in this system"),
    (r"\bLLM\b",                         "say 'AI provider' or name the model"),
    (r"\bprompt engineer(ing)?\b",       "not how this work is positioned"),
    (r"\bproprietary algorithm\b",       "vague and unverifiable"),
    (r"\bcutting-edge\b",                "empty adjective"),
    (r"\bstate-of-the-art\b",            "empty adjective"),
    (r"\bgame-?chang(er|ing)\b",         "empty adjective"),
    (r"\brevolutionary\b",               "empty adjective"),
    (r"\bseamless(ly)?\b",               "empty adjective"),
    (r"\bleverag(e|ing)\b",              "say what was actually used"),

    # rule 3 — provenance, in both directions
    (r"\bdelivered to client\b",         "no engagement happened"),
    (r"\bpaying clients?\b",             "nobody has paid for this system"),
    (r"\bcommissioned\b",                "nobody commissioned this system"),
    (r"\bclient (paid|funded|hired)\b",  "no client paid, funded or hired"),
    (r"\bbuilt for (a|our|the|my) client\b", "built to a public brief"),
    (r"\bdelivered (work|outcomes|systems?)\b", "nothing was delivered"),
    (r"\bpractice project\b",            "this runs — 'practice' is inaccurate"),
    (r"\blearning exercise\b",           "understates a system that runs"),
    (r"\btoy (project|example|system)\b", "understates a system that runs"),
    (r"\bhobby project\b",               "understates a system that runs"),
    (r"\bjust a demo\b",                 "the demo walks a system that runs"),
    (r"\bportfolio filler\b",            "understates a system that runs"),
    (r"\bmock-?up only\b",               "nothing here is a mock-up"),
]

# Allowed because each describes a real API call, not a claim to a discipline.
ALLOWED_PHRASES = [
    "AI provider API (vision)",
    "AI provider API (text)",
    "Photos are sent to an AI provider",
    "Reads listing photos for visible damage",
    "photo read",
    "Photo damage read",
]

NUMBER_CLAIM = re.compile(r"(?<![\w#/])(\d{1,3}(?:\.\d+)?\s?%|\b\d{1,3}x\b|"
                          r"\$\s?\d[\d,]*)", re.I)
SOURCE_WORDS = ("measured", "measurement", "baseline", "not claimed",
                "no efficiency", "without a stated", "no time-saved",
                "unsourced", "verifiable", "counts", "stated method",
                "requires a measured")
# A CSS width or an <img width> is layout, not a promise.
LAYOUT = re.compile(r'(width|height|top|left|right|bottom|flex|opacity|'
                    r'translate|rgba?)\s*[:=]|["\']?\d+%["\']?\s*[;,)]|'
                    r'width\s*=\s*["\']', re.I)

TEXT_EXT = {".md", ".html", ".svg", ".mmd", ".txt", ""}
SKIP_DIRS = {".git", ".github", "__pycache__"}

# One page in this portfolio is a working demo interface rather than prose, and
# an interface has numbers in it — a KPI tile reading 80% is sample data, not a
# claim about anyone's results. The exemption is earned rather than free: the
# page has to say so, visibly, in this exact wording, and then the numeric rule
# is lifted for that file only. Every other rule still applies to it.
SAMPLE_DATA_MARK = "every figure on this page is illustrative"

REQUIRED = ["README.md", "LICENSE", "NOTICE.md", "SECURITY.md",
            "workflows/README.md", "docs/index.html"]
DISCLOSURE = "not been sold or deployed"

problems = []


def check_file(path):
    rel = os.path.relpath(path, ROOT).replace("\\", "/")
    try:
        with open(path, encoding="utf-8") as fh:
            body = fh.read()
    except (UnicodeDecodeError, IsADirectoryError, OSError):
        return
    lines = body.split("\n")
    numbers_are_sample_data = SAMPLE_DATA_MARK in body.lower()

    for i, line in enumerate(lines, 1):
        probe = line
        for ok in ALLOWED_PHRASES:
            probe = probe.replace(ok, "")

        for pat, why in BANNED:
            m = re.search(pat, probe, re.I)
            if m:
                problems.append("%s:%d  banned '%s' - %s\n      %s"
                                % (rel, i, m.group(0), why, line.strip()[:120]))

        if numbers_are_sample_data or LAYOUT.search(line):
            continue
        low = line.lower()
        if "shields.io" in low or any(s in low for s in SOURCE_WORDS):
            continue
        for m in NUMBER_CLAIM.finditer(line):
            problems.append(
                "%s:%d  unsourced numeric claim '%s' - state the measurement "
                "method or remove it\n      %s"
                % (rel, i, m.group(0), line.strip()[:120]))


def check_structure():
    for rel in REQUIRED:
        if not os.path.exists(os.path.join(ROOT, *rel.split("/"))):
            problems.append("MISSING %s" % rel)


def check_disclosure():
    """Present on the README and on the demo, checked separately."""
    for rel in ("README.md", "docs/index.html"):
        fp = os.path.join(ROOT, *rel.split("/"))
        if not os.path.exists(fp):
            continue
        with open(fp, encoding="utf-8") as fh:
            if DISCLOSURE not in fh.read().lower():
                problems.append(
                    "%s: availability disclosure missing - every client-facing "
                    "page must state that the system has not been sold or "
                    "deployed into a customer's business" % rel)


def check_demo_is_self_contained():
    """A demo that calls out to a CDN is a demo that breaks."""
    fp = os.path.join(ROOT, "docs", "index.html")
    if not os.path.exists(fp):
        return
    with open(fp, encoding="utf-8") as fh:
        html = fh.read()
    for pat in (r'src\s*=\s*["\']https?://',
                r'href\s*=\s*["\']https?://[^"\']*\.(css|js)',
                r'@import\s+url\(', r'fonts\.googleapis'):
        if re.search(pat, html, re.I):
            problems.append("docs/index.html: external resource (%s) - the "
                            "demo must open with no network" % pat)


def check_no_workflow_export():
    """The build is not published. Nothing that could be an export ships."""
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if fn.lower().endswith((".json", ".yaml", ".yml")):
                rel = os.path.relpath(os.path.join(dirpath, fn), ROOT)
                problems.append("%s: a workflow export must never be committed"
                                % rel.replace("\\", "/"))


def main():
    # The runner is UTF-8, a Windows console is not. A linter that crashes while
    # printing the line it objected to is worse than useless, so the stream is
    # made total before anything is written to it.
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):
        pass

    check_structure()
    check_disclosure()
    check_demo_is_self_contained()
    check_no_workflow_export()
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if os.path.splitext(fn)[1].lower() in TEXT_EXT:
                check_file(os.path.join(dirpath, fn))

    print("=" * 68)
    if problems:
        print("FAIL - %d problem(s)\n" % len(problems))
        for x in problems:
            print("  " + x)
        print("=" * 68)
        return 1
    print("PASS - scope, honesty and provenance checks clean")
    print("=" * 68)
    return 0


if __name__ == "__main__":
    sys.exit(main())
