#!/usr/bin/env python3
"""PostToolUse hook: bumps `last modified YYYY-MM-DD` in this project's index.html
to today's date whenever Claude edits or writes that file.

Reads Claude Code's hook payload (JSON) from stdin; exits 0 silently on any
non-match so the hook never blocks the tool flow.
"""
import sys, json, re, datetime, os

try:
    payload = json.load(sys.stdin)
except Exception:
    sys.exit(0)

fp = (payload.get("tool_input") or {}).get("file_path") or ""
norm = fp.replace("\\", "/").lower()
if not norm.endswith("agentforce-cost-gateway/index.html"):
    sys.exit(0)
if not os.path.isfile(fp):
    sys.exit(0)

today = datetime.date.today().isoformat().encode("ascii")
pattern = re.compile(rb"last modified \d{4}-\d{2}-\d{2}")

with open(fp, "rb") as f:
    raw = f.read()
new = pattern.sub(b"last modified " + today, raw)
if new != raw:
    with open(fp, "wb") as f:
        f.write(new)
