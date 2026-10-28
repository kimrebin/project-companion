---
name: project-companion
description: Keeps a plain-language, evidence-backed log of what Claude Code actually did on a project and why, written as markdown files the user reads directly — no separate app, dashboard, or database needed. Use this whenever a coding turn just finished real work (files changed, commands run, tests run) in a project that has a .claude/companion/ folder, or when the user asks things like "what did you just change and why", "why did you do it that way", "what have you done so far", "can you explain that in simpler terms", "keep track of this for me", or asks to turn on / set up progress tracking for a project (in any language — e.g. "방금 뭐 바꾼거야", "왜 이렇게 했어", "지금까지 뭐 했어"). This skill IS the review surface — always prefer writing/reading the companion log over just answering from memory when the question is about past work, especially work from an earlier session. Trigger proactively even when the user doesn't name "companion" or "log" explicitly.
---

# Project Companion

## Why this exists

The person working with Claude Code is not always able to read a diff or a stack trace and know what it means. The point of this skill is to make Claude Code's own work legible to that person, at whatever level they're actually at — not to produce a developer changelog. Every entry should answer, in plain terms: what changed, why, and how Claude Code actually knows it worked (not just that it believes it worked).

This replaces building a separate dashboard/database for the same purpose. The markdown files under `.claude/companion/` in the project *are* the dashboard — readable in any editor, versioned by git, with no server to run.

Two hard rules carry over from everything this approach is meant to fix:

1. **Evidence, not vibes.** Only write that something is verified if you actually ran it and are quoting the real output. If you didn't run it, say so plainly — "I didn't actually run this to confirm" is a completely fine thing to write. A confident-sounding claim that turns out to be wrong is worse than an honest "not sure."
2. **Match the reader, not the code.** Avoid unexplained jargon. When a technical term is genuinely necessary, explain it in one short clause right where it's used, calibrated to the project's `PROFILE.md` (see below).

## Language

Write everything this skill produces — profile questions, log entries, section headers, index lines — in the same language the user is actually using with you (match their most recent messages). If the project's `PROFILE.md` was written in a particular language, keep using that language for this project's entries unless the user switches. If the language is unclear or mixed, default to English. Section headers are not fixed strings to copy verbatim — translate them naturally (e.g. "What I did" / "무엇을 했는지" / "¿Qué hice?") so the log reads as if written by a native speaker, not a translated template.

## Step 0: is there a companion set up for this project?

Check for `.claude/companion/` in the project root (relative to the repo you're working in, not the Claude Code install location).

- **Folder exists** → this skill is active for this project. Continue to Step 1.
- **Folder doesn't exist** and the user is asking you to turn this on, or start tracking progress, or something equivalent → create it (see "Setting up a new project" below), then continue.
- **Folder doesn't exist** and this is just a normal coding turn with no such request → don't create it unprompted. Do the coding work normally.

## Step 1: read the profile (first time, or if you haven't this session)

Read `.claude/companion/PROFILE.md`. It's a short, plain-prose note describing who's reading these logs — their technical background, how much detail they want, any terms they've said to avoid or always explain. Let it set your tone, depth, and language for every entry in this project.

If the folder exists but `PROFILE.md` doesn't, ask the user 2-3 short questions before writing your first entry. Ask about **this project specifically**, not just coding in general — someone can be a strong programmer and still be new to what *this* project actually does (its domain, its purpose), or the reverse, and either gap changes what needs explaining:
- How much do you know about what this project actually does, and separately, how much coding experience do you have in general? (Either answer alone is fine — e.g. someone might not know code well but understand exactly why this project exists.)
- Do you prefer short, to-the-point explanations, or more thorough ones?
- Any terms you'd like avoided, or conversely terms you're already comfortable with?

Write the answers as plain prose (not a form) into `PROFILE.md`, in the language the user answered in. Record both axes separately — general coding familiarity AND familiarity with this project's own domain/purpose — since an entry might need to explain a coding concept, a domain concept, both, or neither, depending on what the task touched.

If you're in a context where you can't ask (e.g., invoked automatically mid-turn with no way to prompt), default to writing for a smart person with no coding background, in whatever language the surrounding conversation is in, and leave a one-line note in that day's entry that the profile still needs setting up.

## Step 2: decide whether this turn deserves a log entry

Write an entry when real work happened: files were created/edited, a command was run, tests were run, something was installed or configured. **Skip** turns that were pure conversation — answering a question, explaining code, discussing a plan — with no actual change. One entry per coherent task is right; don't write one per individual tool call, and don't split one piece of work into several entries just because it took several tool calls.

If a Stop hook or other system message explicitly tells you to log the current task, do it even if you'd have judged it borderline — that signal exists specifically to make this reliable instead of depending on your memory each turn.

## Step 3: write the entry

File path: `.claude/companion/log/<YYYY-MM-DD>-<HHMMSS>-<short-slug>.md`, using the current date/time and a short kebab-case slug of what the task was about (e.g. `2026-10-27-143012-add-auto-explain-automation.md`). The slug can stay in English/ASCII even when the entry's prose is in another language — it's just a filename.

Use this structure — keep every section, but the length of each should match what actually happened (a one-line fix doesn't need five paragraphs), and write the headers themselves in the project's language, not literally as shown here:

```markdown
# <one-line title>

- Time: <ISO 8601 timestamp>
- What was asked: <what the user actually requested, one or two lines>

## What I did
<the files changed/created, commands run, described in terms a person can follow. File paths are fine to mention, but explain what that file's role actually is>

## Why I did it this way
<why this approach, and what alternatives were considered and rejected, if any>

## How I actually checked this (evidence)
<paste the real output of commands/tests you actually ran — not a summary like "tests passed", but the real output itself>

## What I'm still not sure about
<anything you didn't verify directly, or that the user won't know for sure until they try it themselves. If genuinely nothing, say so explicitly rather than omitting the section>
```

### When the change is big or touches many files

A one-line fix is easy to narrate. A change spanning several files isn't automatically harder to explain — but it is if you just list every file. Instead:

- Open "What I did" with one or two plain sentences on the overall effect — what can the reader now do, or what's now true, that wasn't before — before any file-level detail. That sentence is what most readers actually need; the rest is for whoever wants to go deeper.
- Group files by the role they played (e.g. "the part the user sees", "the part that saves things", "the part that connects the two") rather than listing paths in isolation. A reader with no coding background can follow "these three files together build one button" far more easily than three unrelated-looking bullet points.
- If more than ~5-6 files changed, summarize the categories and call out only the one or two files that matter most for understanding *why*, rather than enumerating all of them with equal weight.
- The same applies to evidence: paste the output that actually demonstrates the result (e.g. the final test run), not every intermediate command you happened to run while getting there.

## Step 4: update the index

`.claude/companion/log/INDEX.md` is a running list, newest entry first. After writing an entry, prepend one line:

```markdown
- <YYYY-MM-DD HH:MM> [<one-line summary>](<entry-filename>.md)
```

Create the file with just that one line if it doesn't exist yet. Don't rewrite or reorder older lines.

## Answering questions about past work

When asked things like "what have you done so far", "why did you do it that way", "what does this part do" — if the answer concerns work from this session, you likely already know it directly. But if it concerns an earlier session, or you want to give a grounded answer instead of relying on memory, **read `INDEX.md` and the relevant entry file(s) and answer from those** rather than reconstructing from scratch — the log is the source of truth across sessions, and the user may be about to make a decision based on your answer.

## Setting up a new project

When the user asks to turn this on for a project that doesn't have `.claude/companion/` yet:
1. Create `.claude/companion/log/`.
2. Run the profile questions from Step 1 and write `PROFILE.md`.
3. Mention, once, that logging happens automatically whenever real work gets done — they don't need to ask for it each time — but that a Stop hook can be added to *guarantee* it fires every turn instead of relying on your own judgment; that's a separate one-time setup step outside this skill (point them to asking for it if they want it, rather than configuring hooks yourself here).
4. Write a first entry for whatever you were doing right before this request, if anything, so the log doesn't start empty.
