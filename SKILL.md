---
name: project-companion
description: Keeps a plain-language, evidence-backed log of what Claude Code actually did on a project and why, written as markdown files the user reads directly — no separate app, dashboard, or database needed. Use this whenever a coding turn just finished real work (files changed, commands run, tests run) in a project that has a .claude/companion/ folder, or when the user asks things like "방금 뭐 바꾼거야", "왜 이렇게 했어", "지금까지 뭐 했어", "what did you just change and why", "can you explain that in simpler terms", "keep track of this for me", or asks to turn on / set up progress tracking for a project. This skill IS the review surface — always prefer writing/reading the companion log over just answering from memory when the question is about past work, especially work from an earlier session. Trigger proactively even when the user doesn't name "companion" or "log" explicitly.
---

# Project Companion

## Why this exists

The person working with Claude Code is not always able to read a diff or a stack trace and know what it means. The point of this skill is to make Claude Code's own work legible to that person, at whatever level they're actually at — not to produce a developer changelog. Every entry should answer, in plain terms: what changed, why, and how Claude Code actually knows it worked (not just that it believes it worked).

This replaces building a separate dashboard/database for the same purpose. The markdown files under `.claude/companion/` in the project *are* the dashboard — readable in any editor, versioned by git, with no server to run.

Two hard rules carry over from everything this approach is meant to fix:

1. **Evidence, not vibes.** Only write that something is verified if you actually ran it and are quoting the real output. If you didn't run it, say so plainly — "이건 실행해서 확인하지 않았습니다" is a completely fine thing to write. A confident-sounding claim that turns out to be wrong is worse than an honest "모르겠음."
2. **Match the reader, not the code.** Avoid unexplained jargon. When a technical term is genuinely necessary, explain it in one short clause right where it's used, calibrated to the project's `PROFILE.md` (see below).

## Step 0: is there a companion set up for this project?

Check for `.claude/companion/` in the project root (relative to the repo you're working in, not the Claude Code install location).

- **Folder exists** → this skill is active for this project. Continue to Step 1.
- **Folder doesn't exist** and the user is asking you to turn this on, or start tracking progress, or something equivalent → create it (see "Setting up a new project" below), then continue.
- **Folder doesn't exist** and this is just a normal coding turn with no such request → don't create it unprompted. Do the coding work normally.

## Step 1: read the profile (first time, or if you haven't this session)

Read `.claude/companion/PROFILE.md`. It's a short, plain-prose note describing who's reading these logs — their technical background, how much detail they want, any terms they've said to avoid or always explain. Let it set your tone and depth for every entry in this project.

If the folder exists but `PROFILE.md` doesn't, ask the user 2-3 short questions before writing your first entry. Ask about **this project specifically**, not just coding in general — someone can be a strong programmer and still be new to what *this* project actually does (its domain, its purpose), or the reverse, and either gap changes what needs explaining:
- 이 프로젝트가 정확히 뭘 하는 건지, 그리고 코드를 평소에 얼마나 다뤄보셨는지 — 둘 다 자유롭게 말씀해주세요. (한쪽만 알아도 괜찮습니다. 예: 코드는 잘 몰라도 이 프로젝트가 왜 필요한지는 잘 아는 경우도 있으니까요.)
- 설명은 짧게 요점만 vs 꼼꼼하게 풀어서, 어느 쪽이 편하신가요?
- 피해줬으면 하는 용어나, 반대로 익숙한 용어가 있나요?

Write down both axes separately in `PROFILE.md` — general coding familiarity AND familiarity with this project's own domain/purpose — since an entry might need to explain a coding concept, a domain concept, both, or neither, depending on what the task touched.

Write the answers as plain prose (not a form) into `PROFILE.md`. If you're in a context where you can't ask (e.g., invoked automatically mid-turn with no way to prompt), default to writing for a smart person with no coding background, and leave a one-line note in that day's entry that the profile still needs setting up.

## Step 2: decide whether this turn deserves a log entry

Write an entry when real work happened: files were created/edited, a command was run, tests were run, something was installed or configured. **Skip** turns that were pure conversation — answering a question, explaining code, discussing a plan — with no actual change. One entry per coherent task is right; don't write one per individual tool call, and don't split one piece of work into several entries just because it took several tool calls.

If a Stop hook or other system message explicitly tells you to log the current task, do it even if you'd have judged it borderline — that signal exists specifically to make this reliable instead of depending on your memory each turn.

## Step 3: write the entry

File path: `.claude/companion/log/<YYYY-MM-DD>-<HHMMSS>-<short-slug>.md`, using the current date/time and a short kebab-case slug of what the task was about (e.g. `2026-10-27-143012-add-auto-explain-automation.md`).

Use this structure — keep every section, but the length of each should match what actually happened (a one-line fix doesn't need five paragraphs):

```markdown
# <한 줄 제목>

- 시각: <ISO 8601 타임스탬프>
- 어떤 요청으로 시작됐는지: <사용자가 실제로 뭘 요청했는지, 한두 줄>

## 무엇을 했는지
<바뀐 파일/만든 파일/실행한 커맨드를 사람이 이해할 수 있는 말로. 파일 경로는 적어도 되지만, 그 파일이 "뭘 하는 부분인지"를 같이 설명>

## 왜 이렇게 했는지
<이 방법을 고른 이유, 고려했던 다른 방법과 버린 이유 (있다면)>

## 실제로 어떻게 확인했는지 (증거)
<진짜로 실행한 커맨드/테스트의 실제 출력을 그대로 인용. "테스트를 통과했습니다" 같은 요약이 아니라 진짜 출력 일부를 붙여넣기>

## 아직 확실하지 않은 것
<직접 실행/확인하지 못한 부분, 사용자가 실제로 써보기 전엔 모르는 부분을 솔직하게. 없으면 "특별히 없음"이라고 명시>
```

### When the change is big or touches many files

A one-line fix is easy to narrate. A change spanning several files isn't automatically harder to explain — but it is if you just list every file. Instead:

- Open `무엇을 했는지` with one or two plain sentences on the overall effect — what can the reader now do, or what's now true, that wasn't before — before any file-level detail. That sentence is what most readers actually need; the rest is for whoever wants to go deeper.
- Group files by the role they played (e.g. "화면에 보이는 부분", "저장하는 부분", "그 둘을 연결하는 부분") rather than listing paths in isolation. A reader with no coding background can follow "이 세 파일은 같이 묶어서 하나의 버튼을 만들었습니다" far more easily than three unrelated-looking bullet points.
- If more than ~5-6 files changed, summarize the categories and call out only the one or two files that matter most for understanding *why*, rather than enumerating all of them with equal weight.
- The same applies to evidence: paste the output that actually demonstrates the result (e.g. the final test run), not every intermediate command you happened to run while getting there.

## Step 4: update the index

`.claude/companion/log/INDEX.md` is a running list, newest entry first. After writing an entry, prepend one line:

```markdown
- <YYYY-MM-DD HH:MM> [<한 줄 요약>](<entry-filename>.md)
```

Create the file with just that one line if it doesn't exist yet. Don't rewrite or reorder older lines.

## Answering questions about past work

When asked things like "지금까지 뭐 했어", "왜 이렇게 했어", "이게 뭐하는 부분이야" — if the answer concerns work from this session, you likely already know it directly. But if it concerns an earlier session, or you want to give a grounded answer instead of relying on memory, **read `INDEX.md` and the relevant entry file(s) and answer from those** rather than reconstructing from scratch — the log is the source of truth across sessions, and the user may be about to make a decision based on your answer.

## Setting up a new project

When the user asks to turn this on for a project that doesn't have `.claude/companion/` yet:
1. Create `.claude/companion/log/`.
2. Run the profile questions from Step 1 and write `PROFILE.md`.
3. Mention, once, that logging happens automatically whenever real work gets done — they don't need to ask for it each time — but that a Stop hook can be added to *guarantee* it fires every turn instead of relying on your own judgment; that's a separate one-time setup step outside this skill (point them to asking for it if they want it, rather than configuring hooks yourself here).
4. Write a first entry for whatever you were doing right before this request, if anything, so the log doesn't start empty.
