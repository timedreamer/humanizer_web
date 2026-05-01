# Repository Guidelines

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

---

**These guidelines are working if:** fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, and clarifying questions come before implementation rather than after mistakes.
---

## Scope & Precedence
- Apply these rules unless directly overridden by user instruction.
- Conflict order: (1) user instruction, (2) this guide, (3) generic assistant defaults.

## Documentation
- Save non-report markdown files under `doc/`.
- Sub-folders under `doc/` are allowed.
- Prefix all generated markdown filenames with `YYYYMMDD` (example: `20260219_implementation_summary.md`).
- **Plans:** All plan documents — regardless of which skill or tool produces them — MUST be saved to `doc/plans/`. Never use `docs/plans/` or any other path. This rule strictly supersedes any default path specified inside skill source files (e.g., brainstorming, writing-plans, executing-plans).
- If asked to write a report, always use Markdown format (`.md`).
- In every report, include the exact scripts or commands used to generate the results, so that the results can be independently reproduced.

## Environment & Installation (No sudo)
- Assume no `sudo` access.
- Keep installs user-local and reproducible.
- Ensure `$HOME/.local/bin` is on `PATH`.
- Package/tool install priority:
  1. `mamba`
  2. standalone user-space binary
  3. `conda`
  4. `uv` (Python packages only)
  5. `pip`
- If installation fails, report the cause and provide concrete next options.

## Quality Tools
- Use `ruff` for lint/format and `pyright` for static type checks.
- Tool configuration lives in `pyproject.toml`.

## Quality Checks
- During iteration (changed files):
  - `ruff check <changed_files> --fix`
  - `ruff format <changed_files>`
- Before handoff:
  - `ruff check . --fix`
  - `ruff format .`
  - `pyright`
  - `python -m pytest`

## Workflow Enforcement
- Run `pyright` after changes affecting more than one file or a shared/core module.
- Core/shared module: utility logic imported by multiple scripts/modules.
- Explicitly report type-check pass/fail.
- If type checks fail, fix relevant errors before handoff.

## Python Style
- Target Python ≥ 3.11.
- Follow PEP 8; use 4-space indentation and `snake_case`.
- Prefer explicit names over abbreviations.
- Prefer `pathlib` over `os.path` where feasible.
- Prefer f-strings over `.format()` / `%`.
- Add type hints; prefer `collections.abc` abstract types where useful.
- Use Google-style docstrings for all public functions, classes, and methods.
- Guard entry points with `if __name__ == "__main__"`:
- No wildcard imports.
- Use `logging` (not `print`) in serious/production code.
- Prefer `enumerate()` over manual counters.
- Avoid hard-coded absolute paths.

## Project Structure
- Put reusable logic in importable modules under `src/`.
- Keep runnable scripts thin (arg parsing + orchestration).
- Save all scripts under domain-specific subfolders within `src/` (e.g., `src/pipeline/`, `src/eval/`); do not place scripts directly in `src/`.
- Use ordered step script names within subfolders when applicable: `01_...py`, `02_...py`, `03_...py`.

## Logging Baseline
- Use `logging.getLogger(__name__)`.
- Use consistent levels: `DEBUG`, `INFO`, `WARNING`, `ERROR`.
- Include stable identifiers in workflow logs when available (e.g., `run_id`, `gene`, `pmid`).


## Data & Secret Hygiene
- Never commit credentials, keys, tokens, or secrets.
- Keep large generated artifacts in designated output folders (for example, `result/`).
- Do not commit caches, temp files, or local environment folders.
- Update `.gitignore` for new generated artifact patterns.

## Testing, Commits, PRs
- Add `pytest` tests (`tests/test_*.py`) for reusable/shared logic; run `python -m pytest`.
- One-off scripts may use lightweight validation unless promoted to reusable workflow logic.
- Prefer Conventional Commits (`feat: ...`, `fix: ...`).
- If asked to commit and/or open a PR, proceed without waiting for approval. Pause for explicit approval only before destructive or high-impact git actions (for example, `git reset --hard`, `git push --force`, deleting branches, rebasing shared branches, or merging directly into `main`).
- If asked to commit all changes, split into logical commits when appropriate.
- In PRs: state goal, list impacted artifacts (especially under `data/`), and include a small command/output example when behavior changes.
