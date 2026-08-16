#!/usr/bin/env python3
"""Layer-1 contribution lint (deterministic, no model — injection-immune).

L1 catches the UNOBFUSCATED forms of capability grants, exfil URLs, and
authority-surface tampering. It is not the whole defense — L2 (model review)
and human promotion (ADR-012, merge != deploy) are load-bearing. See
SECURITY.md.

Modes:
  --base REF     lint `git diff REF...HEAD`; frontmatter range is read from
                 the actual on-disk file, NOT inferred from the diff (a diff
                 with unchanged --- delimiters must not hide a grant).
  --files F...   lint whole files as fully-added (corpus + diff-mode fixtures)

Exit 1 on any FAIL. AREOS_LINT_ALLOW_AUTHORITY=1 (CI: `authority-ok` label,
maintainer-only) permits authority-surface changes.
"""
import os
import re
import subprocess
import sys
from urllib.parse import urlsplit

AUTHORITY_PREFIXES = ("CLAUDE.md", ".claude/", ".github/", "scripts/")
CORPUS_DIR = "tests/injection-corpus/"

CAPABILITY_RE = re.compile(
    r"^\s*(allowed-tools|hooks|context|agent|shell|paths)\s*:", re.I)
DMI_FALSE_RE = re.compile(r"^\s*disable-model-invocation\s*:\s*false", re.I)
DMI_TRUE_RE = re.compile(r"^\s*disable-model-invocation\s*:\s*true", re.I)
INVISIBLE_RE = re.compile(
    "[\u200b-\u200f\u202a-\u202e\u2060-\u2064\u2066-\u2069\u00ad\ufeff]")
SCHEME_URL_RE = re.compile(r"(?:https?:)?//([^\s/@]+@)?([A-Za-z0-9.\-]+)")
BARE_DOMAIN_RE = re.compile(
    r"\b([A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?"
    r"(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?)*"
    r"\.[A-Za-z][A-Za-z0-9-]*[A-Za-z])"  # final label must contain a letter
    r"/[A-Za-z0-9]")  # domain.tld/path — the exfil shape, scheme or not; a
    # numeric-only last label (0.63/x, v1.2/x) is never a domain
BLOB_RE = re.compile(r"[A-Za-z0-9+/=]{200,}")

def allowed_domains():
    path = os.path.join(os.path.dirname(__file__), "..", ".github",
                        "allowed-domains.txt")
    try:
        with open(path, encoding="utf-8") as f:
            return {l.strip() for l in f
                    if l.strip() and not l.startswith("#")}
    except FileNotFoundError:
        return set()

def domain_ok(dom):
    dom = dom.lower().rstrip(".")
    return dom in ALLOWED or any(dom.endswith("." + a) for a in ALLOWED)

def frontmatter_range(path):
    """Real leading ---...--- line range [start,end] (1-indexed), or None.
    Read from disk so a diff can't hide the boundary."""
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            lines = f.read().splitlines()
    except OSError:
        return None
    if not lines or lines[0].strip() != "---":
        return None
    for i in range(1, min(len(lines), 60)):
        if lines[i].strip() == "---":
            return (1, i + 1)
    return None

def scan_content(path, n, line, fails, in_fm):
    if path.startswith(CORPUS_DIR):
        return
    if INVISIBLE_RE.search(line):
        fails.append(f"FAIL {path}:{n}: invisible/bidi unicode character")
    if BLOB_RE.search(line):
        fails.append(f"FAIL {path}:{n}: base64-like blob (>=200 chars)")
    for m in SCHEME_URL_RE.finditer(line):
        host = m.group(2)
        if host and not domain_ok(host):
            fails.append(f"FAIL {path}:{n}: URL host '{host}' not allowlisted")
    for m in BARE_DOMAIN_RE.finditer(line):
        host = m.group(1)
        if not domain_ok(host):
            fails.append(f"FAIL {path}:{n}: domain '{host}' not allowlisted")
    if in_fm and CAPABILITY_RE.match(line):
        fails.append(f"FAIL {path}:{n}: capability frontmatter "
                     f"'{line.strip()[:40]}' (maintainer-only)")
    if in_fm and DMI_FALSE_RE.match(line):
        fails.append(f"FAIL {path}:{n}: disable-model-invocation:false "
                     "(enables auto-invocation; maintainer-only)")

def lint_diff(base):
    fails, authority = [], []
    diff = subprocess.run(["git", "diff", f"{base}...HEAD", "--unified=0"],
                          capture_output=True, text=True, check=True).stdout
    # collect added lines per file, plus removed DMI:true (a removal, so it
    # will not be an added line)
    added = {}       # path -> list[(n, line)]
    path, n = None, 0
    for raw in diff.splitlines():
        if raw.startswith("diff --git a/"):
            m = re.match(r"diff --git a/(.*) b/(.*)", raw)
            path = m.group(2) if m else None  # so mode-line FAILs name the file
            continue
        if raw.startswith("+++ b/"):
            path = raw[6:]
            added.setdefault(path, [])
            if path.startswith(AUTHORITY_PREFIXES):
                authority.append(path)
            continue
        if raw.startswith("Binary files") and " differ" in raw:
            fails.append(f"FAIL binary file change: {raw}")
            continue
        if raw.startswith("new file mode 120000") \
                or raw.startswith("new mode 120000"):
            fails.append(f"FAIL {path}: introduces a symlink "
                         "(120000) — not allowed in contributions")
            continue
        m = re.match(r"^@@ -\d+(?:,\d+)? \+(\d+)", raw)
        if m:
            n = int(m.group(1)) - 1
            continue
        if raw.startswith("+") and not raw.startswith("+++"):
            n += 1
            added[path].append((n, raw[1:]))
        elif raw.startswith("-") and not raw.startswith("---"):
            if path and DMI_TRUE_RE.match(raw[1:]) \
                    and not path.startswith(CORPUS_DIR):
                fails.append(f"FAIL {path}: removes "
                             "'disable-model-invocation: true'")
    for path, lines in added.items():
        fm = frontmatter_range(path)  # real range from disk (merge checkout)
        for n, line in lines:
            in_fm = fm is not None and fm[0] <= n <= fm[1]
            scan_content(path, n, line, fails, in_fm)
    if authority and os.environ.get("AREOS_LINT_ALLOW_AUTHORITY") != "1":
        for p in sorted(set(authority)):
            fails.append(f"FAIL authority surface changed: {p} "
                         "(maintainer-only; needs 'authority-ok' label)")
    return fails

def lint_files(paths):
    fails = []
    for path in paths:
        rel = os.path.relpath(path)
        if os.path.islink(path):
            fails.append(f"FAIL {rel}: symlink (not allowed in contributions)")
            continue
        fm = frontmatter_range(path)
        with open(path, encoding="utf-8", errors="replace") as f:
            for n, line in enumerate(f, 1):
                in_fm = fm is not None and fm[0] <= n <= fm[1]
                scan_content(rel, n, line.rstrip("\n"), fails, in_fm)
    return fails

if __name__ == "__main__":
    ALLOWED = allowed_domains()
    args = sys.argv[1:]
    if args[:1] == ["--base"]:
        failures = lint_diff(args[1])
    elif args[:1] == ["--files"]:
        failures = lint_files(args[1:])
    else:
        sys.exit(__doc__)
    for f in failures:
        print(f)
    print(f"contribution-lint: {len(failures)} failure(s)")
    sys.exit(1 if failures else 0)
