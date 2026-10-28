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
            print(f"기존 설정 파일을 읽는 데 실패했습니다 ({settings_path}): {e}")
            print("JSON 문법이 깨져 있을 수 있습니다. 직접 확인해 주세요.")
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
    print(f"완료: {settings_path} 에 project-companion Stop 훅을 등록했습니다.")
    print("Claude Code를 쓰는 모든 프로젝트에 적용되지만, 실제로 .claude/companion/")
    print("폴더가 있는 프로젝트에서만 동작합니다. 이미 실행 중인 Claude Code 세션이")
    print("있다면 한 번 재시작하거나 /hooks 메뉴를 열어 설정을 다시 불러오세요.")


if __name__ == "__main__":
    main()
