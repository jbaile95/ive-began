# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Run the CLI calculator
python main.py

# Run the Flask web app (dev server at http://127.0.0.1:5000)
python app.py

# Install dependencies
pip install -r requirements.txt
```

## Architecture

The project has two independent interfaces that share the same `Calculator` class:

- [calculator.py](calculator.py) — `Calculator` class with static methods: `add`, `subtract`, `multiply`, `divide`, `power`, `sqrt`, `log`, `modulo`. All operations raise `ZeroDivisionError` or `ValueError` on invalid input.
- [main.py](main.py) — interactive CLI loop; prompts user for operation and two numbers, calls `Calculator` methods directly.
- [app.py](app.py) — Flask web app exposing two routes:
  - `GET /` → serves [templates/index.html](templates/index.html) (basic two-operand calculator, POSTs JSON to `POST /calculate`)
  - `POST /calculate` → validates inputs, dispatches to `Calculator`, returns JSON `{result}` or `{error}`
  - `GET /advanced` → serves [templates/advanced.html](templates/advanced.html) (button/keyboard-driven calculator UI that POSTs raw expression strings to `POST /evaluate`)

## Notes

- `POST /evaluate` uses a safe AST-based evaluator (no `eval()`). Supports `+`, `-`, `*`, `/`, `**`, `%`, and the functions `sqrt()` and `log()` (which maps to `log10`).
- One-argument operations (`sqrt`, `log10`) skip the second number prompt in the CLI and the second number field in the basic web UI.
- The advanced UI sends raw expression strings (e.g. `sqrt(16)`, `2**8`) to `/evaluate`; `^` typed on the keyboard is converted to `**` client-side before sending.

Behavioral guidelines to reduce common LLM coding mistakes. Merge with project-specific instructions as needed.

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