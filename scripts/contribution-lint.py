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
# Files loaded as authority by name at ANY depth, not just root: the harness
# reads CLAUDE.md from subdirectories, and .mcp.json registers MCP servers
# (a tool grant). A prefix match on root alone misses "docs/CLAUDE.md" and
# ".mcp.json".
AUTHORITY_BASENAMES = ("CLAUDE.md", ".mcp.json")
CORPUS_DIR = "tests/injection-corpus/"


def is_authority(path):
    return (path.startswith(AUTHORITY_PREFIXES)
            or path.rsplit("/", 1)[-1] in AUTHORITY_BASENAMES)

# Capability keys are matched by YAML shape, not one fixed line form: a key may
# be quoted ("allowed-tools":) or live in a single-line flow mapping
# ({..., allowed-tools: ...}), and both parse to the same top-level key. So the
# block forms tolerate an optional quote, and flow mappings are scanned too.
CAPABILITY_KEYS = ("allowed-tools", "hooks", "context", "agent", "shell", "paths")
_CAP_ALT = "|".join(CAPABILITY_KEYS)
CAPABILITY_RE = re.compile(r"^\s*[\"']?(" + _CAP_ALT + r")[\"']?\s*:", re.I)
# YAML explicit-key form: "? allowed-tools" on one line, ": [...]" on the next,
# parses to the same top-level key but has no trailing ':' for CAPABILITY_RE to
# match. Flag the '? <cap-key>' line; the explicit-key shape for a capability
# key in frontmatter is itself anomalous.
EXPLICIT_KEY_RE = re.compile(
    r"^\s*\?\s*[\"']?(" + _CAP_ALT + r"|disable-model-invocation)\b", re.I)
DMI_FALSE_RE = re.compile(
    r"^\s*[\"']?disable-model-invocation[\"']?\s*:\s*false", re.I)
DMI_TRUE_RE = re.compile(
    r"^\s*[\"']?disable-model-invocation[\"']?\s*:\s*true", re.I)
# A key inside a single-line flow mapping, i.e. preceded by its delimiter { or ,
# and optionally quoted. Applied only to lines that open a flow mapping, so a
# comma in ordinary prose cannot trigger it.
FLOW_KEY_RE = re.compile(
    r"[{,]\s*[\"']?(" + _CAP_ALT + r"|disable-model-invocation)[\"']?\s*:\s*([^,}]*)",
    re.I)
INVISIBLE_RE = re.compile(
    "[\u00ad\u180e\u200b-\u200f\u202a-\u202e\u2060-\u2064\u2066-\u2069"
    "\ufe00-\ufe0f\ufeff]"           # soft hyphen, MVS, zero-width/bidi, VS
    "|[\U000e0000-\U000e007f]")      # Unicode tag block (hidden-ASCII smuggling)
SCHEME_URL_RE = re.compile(r"(?:https?:)?//([^\s/@]+@)?([A-Za-z0-9.\-]+)")
# A bare IPv4 endpoint with a path (no scheme): domains route through the
# allowlist, but an IP is never allowlistable and BARE_DOMAIN_RE excludes a
# numeric final label, so a scheme-less "1.2.3.4/collect" would otherwise slip.
IPV4_PATH_RE = re.compile(r"\b((?:\d{1,3}\.){3}\d{1,3})(?::\d+)?/[A-Za-z0-9]")
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
    for i in range(1, len(lines)):
        # '...' is a valid YAML document-end terminator that frontmatter
        # parsers accept; treat it as a close too, else a grant hidden behind
        # a '...' close would leave the range unfound.
        if lines[i].strip() in ("---", "..."):
            return (1, i + 1)
    # Opened with '---' but never terminated. Fail CLOSED: scan the whole file
    # as frontmatter rather than returning None (which would silently disable
    # every capability check on the file).
    return (1, len(lines))

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
    for m in IPV4_PATH_RE.finditer(line):
        fails.append(f"FAIL {path}:{n}: bare IP endpoint "
                     f"'{m.group(1)}' (exfil shape; IPs are never allowlisted)")
    if in_fm and CAPABILITY_RE.match(line):
        fails.append(f"FAIL {path}:{n}: capability frontmatter "
                     f"'{line.strip()[:40]}' (maintainer-only)")
    if in_fm and EXPLICIT_KEY_RE.match(line):
        fails.append(f"FAIL {path}:{n}: capability key in YAML explicit-key "
                     f"form '{line.strip()[:40]}' (maintainer-only)")
    if in_fm and DMI_FALSE_RE.match(line):
        fails.append(f"FAIL {path}:{n}: disable-model-invocation:false "
                     "(enables auto-invocation; maintainer-only)")
    if in_fm and line.lstrip().startswith("{"):
        for m in FLOW_KEY_RE.finditer(line):
            key = m.group(1).lower()
            if key in CAPABILITY_KEYS:
                fails.append(f"FAIL {path}:{n}: capability '{key}' in flow "
                             "mapping (maintainer-only)")
            elif (key == "disable-model-invocation"
                  and m.group(2).strip().strip("\"'").lower() == "false"):
                fails.append(f"FAIL {path}:{n}: disable-model-invocation:false "
                             "in flow mapping (maintainer-only)")

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
            if is_authority(path):
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
