#!/usr/bin/env python3
"""One-time setup: registers this skill's Stop hook in the user's global
Claude Code settings (~/.claude/settings.json). Safe to run more than once.
"""
import json
import sys
from pathlib import Path

MARKER_KEY = "_project_companion_managed"


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    settings_path = Path.home() / ".claude" / "settings.json"
    script_path = (Path(__file__).resolve().parent / "stop_reminder.py")

    if settings_path.exists():
        try:
            settings = json.loads(settings_path.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"Could not read existing settings file ({settings_path}): {e}")
            print("It may have invalid JSON — please check it manually.")
            sys.exit(1)
    else:
        settings = {}
        settings_path.parent.mkdir(parents=True, exist_ok=True)

    hooks = settings.setdefault("hooks", {})
    stop_entries = hooks.setdefault("Stop", [])

    # remove any entry this skill previously added, so re-running is idempotent
    for entry in list(stop_entries):
        entry["hooks"] = [h for h in entry.get("hooks", []) if not h.get(MARKER_KEY)]
    stop_entries[:] = [e for e in stop_entries if e.get("hooks")]

    command = f'python "{script_path}"'
    stop_entries.append({
        "hooks": [
            {
                "type": "command",
                "command": command,
                "async": False,
                MARKER_KEY: True,
            }
        ]
    })

    settings_path.write_text(
        json.dumps(settings, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Done: registered the project-companion Stop hook in {settings_path}")
    print("It applies across every project you use Claude Code in, but only does")
    print("anything in projects that actually have a .claude/companion/ folder.")
    print("If you have a Claude Code session already running, restart it or open")
    print("the /hooks menu once to reload settings.")


if __name__ == "__main__":
    main()
