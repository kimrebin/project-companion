# Project Companion

A [Claude Code skill](https://docs.claude.com/en/docs/claude-code/skills) that keeps a plain-language, evidence-backed log of what Claude actually did on your project — written straight to markdown files in your repo. No dashboard, no server, no database to run.

## "I can just ask Claude to log things, why do I need this?"

You can, but try it a few times in a row and you'll notice what you actually get:

- **A different format every time.** One turn it writes `PROGRESS.md`, the next it writes `notes/2026-10-27.txt`, the next it just tells you in chat and writes nothing. Nothing is at a predictable path, so you can't build a habit of checking "the log."
- **You have to remember to ask, every single time.** Forget once and that turn is gone. Multiply that by a long session and your history has holes in exactly the places you'd most want it.
- **It reports what it believes, not what it checked.** "Tests pass" is a claim. This skill makes Claude paste the *actual* command output — a real pytest failure, then a real pytest pass — so the log is evidence, not a summary of its own confidence.
- **It explains at one fixed level, usually "developer."** This skill keeps a short profile per project (your coding background **and** how well you know *this specific project*) and writes every entry to match it — plain language, analogies, no unexplained jargon, grouped by what a part of the system actually does rather than a flat list of filenames.
- **It forgets what it decided not to log.** A pure Q&A turn ("what does this function do?") correctly produces *no* entry — so the log stays signal, not noise — and that's a deliberate rule, not something that happens to be true this one time.

Paired with one small Stop hook (installed once, globally), Claude checks on every turn whether that turn's work is worth logging — instead of relying on you to remember to ask.

## Install

```bash
git clone https://github.com/kimrebin/project-companion ~/.claude/skills/project-companion
python "~/.claude/skills/project-companion/scripts/install_hook.py"
```

The second command adds one Stop hook to your global Claude Code settings (`~/.claude/settings.json`). It only touches that one entry — your existing settings are left alone — and running it again is a no-op, not a duplicate. Skipping it still lets the skill work, just relying on Claude's own judgment each turn instead of a guaranteed check.

## Usage

No slash commands to memorize — just talk to Claude normally.

1. In any project you want tracked, ask Claude in plain language:
   > "Turn on progress tracking for this project."

   The first time, it asks a couple of quick questions (your coding background, and how familiar you are with *this* project specifically) so it knows how to calibrate future entries.

2. From then on, every turn that actually changes something gets a dated entry under `.claude/companion/log/`, automatically.

3. To review: open the markdown files directly, or just ask Claude — "what have you done so far?", "why did you do it that way?" — and it reads the log instead of guessing from memory.

## Uninstall

- Per project: delete that project's `.claude/companion/` folder.
- Everywhere: delete `~/.claude/skills/project-companion/`, and remove the entry tagged `"_project_companion_managed": true` from `hooks.Stop` in `~/.claude/settings.json` (leave the rest of that file as-is).
