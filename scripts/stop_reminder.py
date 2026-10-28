#!/usr/bin/env python3
import json
import sys
from pathlib import Path


def _force_utf8_streams():
    try:
        sys.stdin.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def main():
    _force_utf8_streams()
    try:
        payload = json.loads(sys.stdin.read())
    except Exception:
        return

    if payload.get("stop_hook_active"):
        return

    cwd = payload.get("cwd")
    if not cwd:
        return

    if not (Path(cwd) / ".claude" / "companion").is_dir():
        return

    reason = (
        "This project has the project-companion skill turned on. If this turn actually "
        "changed files or ran commands/tests, follow the project-companion skill (SKILL.md) "
        "to write an entry under `.claude/companion/log/` and update `INDEX.md` — in the "
        "language you've been using with the user. If this turn was pure Q&A/explanation "
        "with no real change, do nothing and just end normally."
    )
    try:
        print(json.dumps({"decision": "block", "reason": reason}, ensure_ascii=False))
    except Exception:
        pass


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
