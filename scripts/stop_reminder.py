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
        "이 프로젝트는 project-companion 스킬이 켜져 있습니다. 방금 턴에서 실제로 파일을 "
        "바꾸거나 커맨드/테스트를 실행했다면, project-companion 스킬(SKILL.md)의 지침대로 "
        "`.claude/companion/log/`에 기록을 남기고 `INDEX.md`를 갱신하세요. 순수 질문/설명만 "
        "한 턴이었다면 아무것도 하지 말고 그대로 끝내세요."
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
