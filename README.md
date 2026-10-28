# Project Companion

Claude Code가 작업할 때, 그 내용을 사람이 알아볼 수 있는 말로 `.claude/companion/` 폴더 안에 기록으로 남겨주는 [Claude Code 스킬](https://docs.claude.com/en/docs/claude-code/skills)입니다. 별도 서버나 대시보드 없이, 프로젝트 안의 markdown 파일로 바로 확인할 수 있습니다.

- 실제로 파일을 바꾸거나 커맨드/테스트를 실행한 턴만 기록합니다 (단순 질문/설명 턴은 기록하지 않음).
- 기록에는 요약된 "테스트 통과했습니다" 식이 아니라, 실제로 실행한 커맨드/테스트의 출력을 그대로 인용합니다.
- 읽는 사람의 코딩 경험 및 그 프로젝트에 대한 이해도에 맞춰 말투와 깊이를 조절합니다 (프로젝트별 `PROFILE.md`에 저장).

## 설치

```bash
git clone https://github.com/kimrebin/project-companion ~/.claude/skills/project-companion
python "~/.claude/skills/project-companion/scripts/install_hook.py"
```

두 번째 명령은 Claude Code의 전역 설정(`~/.claude/settings.json`)에 Stop 훅 하나를 추가합니다. 작업이 끝날 때마다 "지금 기록할 게 있는지" 확인하도록 해서, 기록이 누락되지 않게 해줍니다. 기존 설정은 건드리지 않고 추가만 하며, 여러 번 실행해도 중복되지 않습니다. 이 단계를 건너뛰어도 스킬 자체는 동작하지만, Claude의 자체 판단에만 의존하게 됩니다.

## 사용법

슬래시 명령어를 외워서 칠 필요는 없습니다. 평소처럼 Claude Code를 쓰면 됩니다.

1. 기록을 켜고 싶은 프로젝트에서 Claude에게 말로 요청하세요:
   > "이 프로젝트 진행 상황 기록 켜줘"

   처음 켤 때 코딩 경험과 이 프로젝트를 얼마나 아는지 몇 가지 물어보고, 그 답을 바탕으로 앞으로의 기록 수준을 맞춥니다.

2. 그 다음부터는 실제 작업이 있을 때마다 `.claude/companion/log/`에 자동으로 기록이 쌓입니다.

3. 기록을 보고 싶으면 그 폴더의 markdown 파일을 직접 열거나, Claude에게 "지금까지 뭐 했어?", "왜 이렇게 했어?"처럼 물어보면 됩니다.

## 끄기 / 제거

- 특정 프로젝트에서만 끄려면: 그 프로젝트의 `.claude/companion/` 폴더를 지우면 됩니다.
- 전체를 제거하려면: 이 스킬 폴더(`~/.claude/skills/project-companion/`)를 지우고, `~/.claude/settings.json`의 `hooks.Stop` 안에서 `"_project_companion_managed": true`가 달린 항목을 지우세요.
