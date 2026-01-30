# Learning Repository Conventions

**Purpose:** This repo is for live coding in class. Code should be easy to read and explore, with minimal complexity. These conventions **override** normal production best practices for this repository only.

---

## Overrides (Do NOT apply here)

| Normal best practice | In this repo |
|----------------------|--------------|
| Centralized logging module | **No.** Use `print()` or simple inline logging when needed. No logging framework or shared logger. |
| Robust error handling / custom exceptions | Keep it minimal. Fail fast with clear errors; avoid deep try/except or custom exception hierarchies. |
| Feature flags, config switches | **No.** Straight-line code only. |
| Production-ready structure (env vars, secrets management, etc.) | **No.** Hardcode or use minimal config only so demos run immediately. |
| Heavy integration tests, test harnesses | Optional. Prefer "run and see" over full test suites when teaching. |
| requirements.md in /plans | Optional for tiny demos; include only when dependencies exist. |

---

## Goals for this repo

1. **Legible and clean** — Code is read in class. Favor clarity over cleverness.
2. **Minimum external requirements** — Fewest dependencies; prefer stdlib. Add a package only when it’s essential for the lesson.
3. **Simplest code that runs** — Correct and runnable, but not productionized. No extra layers (middleware, abstractions, frameworks) unless the lesson requires them.
4. **Fewest lines possible** — Prefer short, self-contained scripts. No boilerplate that doesn’t directly support the lesson.
5. **Explorable in class** — File and variable names should make intent obvious. One main idea per file or section when possible.

---

## Code style (this repo)

- **Python preferred** when possible.
- **No single-letter variable names** — use short but meaningful names (`count`, `item`, `result`).
- **No commenting out features** to simplify — if something isn’t needed for the lesson, remove it or put it in a separate example file.
- **Virtual environment** — use `./venv` or `./env`; no Conda.
- **No hallucination** — only use patterns and APIs you can verify (e.g. from docs).

---

## What to include

- **Plan and requirements** in `/plans` (e.g. `plan.md`, and `requirements.md` only when deps exist).
- **Devlog/diary** in `/devlog` for complex or multi-step work, when useful for the class narrative.
- **One clear idea per example** — separate files or folders for different concepts so students can open and run one thing at a time.

---

## Summary

For this learning repo: **readable, minimal, runnable.** Optimize for “we can read and run this in class” over “this is production-ready.”
