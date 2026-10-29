# Project Companion

When Claude Code finishes a task, it reports back the way it would to another developer who already knows the codebase — full of implementation detail, assuming shared context. But the people actually reading that report don't all share that context. Some have never written code. Some code for a living but are brand new to *this particular* project. Some fall somewhere in between. A report written for "a developer who already knows this codebase" leaves most of those people unable to actually follow, question, or trust what the AI just did — which defeats the whole point of having a human review AI-driven work in the first place.

**Project Companion** is a Claude Code skill that writes a plain-language, evidence-backed log of what Claude actually did — calibrated to the specific person reading it, not to a generic "technical" reader — straight into markdown files in your repo. No dashboard, no server, no database.

## The problem this solves

Two things vary independently from person to person, and most AI-written reports account for neither:

- **How much coding experience you have, in general.**
- **How well you know *this specific project*** — its purpose, its structure, why it's built the way it is. Someone can be a strong engineer and still be completely new to this codebase; someone else can barely code and still understand exactly why the project exists and what it's for.

A report pitched at "developer who already knows this codebase" is wrong for almost everyone except the person who wrote the code. This skill keeps a short profile per project that records both of those axes separately, and writes every entry to match them — plain language, analogies instead of jargon, technical terms explained inline instead of assumed, grouped by what each part of the system actually *does* rather than a flat list of filenames you have no reason to recognize. The goal is that someone can open the log and actually follow what happened and why, at their own level — not just see that *something* happened.

## "I can just ask Claude to log things, why do I need this?"

You can, but try it a few times in a row and you'll notice what you actually get:

- **It still explains at one fixed level — usually "developer."** Asking "please log what you did" doesn't tell Claude how much you know about coding, or about this project. Without that, it defaults to the same jargon-heavy, assume-the-reader-knows-the-codebase register this skill exists to avoid.
- **A different format every time.** One turn it writes `PROGRESS.md`, the next it writes `notes/2026-10-27.txt`, the next it just tells you in chat and writes nothing. Nothing is at a predictable path, so you can't build a habit of checking "the log."
- **You have to remember to ask, every single time.** Forget once and that turn is gone. Multiply that by a long session and your history has holes in exactly the places you'd most want it.
- **It reports what it believes, not what it checked.** "Tests pass" is a claim. This skill makes Claude paste the *actual* command output — a real pytest failure, then a real pytest pass — so the log is evidence, not a summary of its own confidence.
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
