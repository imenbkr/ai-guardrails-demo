# AI-generated code under control: demo repo

A 10-minute live demo for a Tech Lunch / short workshop.

The story in one line: **AI wrote this code. Each guardrail catches something the
previous one missed, and a good harness makes the AI catch its own mistakes.**

| Layer | Tool | Catches in this repo |
|---|---|---|
| 1. Lint & format | pre-commit + ruff | unused imports, bare `except`, mutable default argument |
| 2. Tests from the spec | pytest | percent > 100 accepted, "10 orders" not counted as loyal |
| 3. AI review | Claude Code | `price_cart` silently changes the caller's cart (tests still pass!) |
| 4. Harness | CLAUDE.md + hooks | the agent runs the checks itself, fixes its own errors, and can't edit the tests |

## Setup (once, ~10 min)

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
git init && git add . && git commit -m "AI-generated pricing module"
pre-commit install
```

Optional for steps 3 and 4: Claude Code installed and logged in
(see https://code.claude.com/docs). Everything else works without it.

## Demo script (~10 min)

**0. The code (1 min).** Open `src/shop/pricing.py`. It has docstrings, constants,
type hints. *"Would you approve this PR?"* Then open `SPEC.md`.

**1. Lint (2 min).**
```bash
pre-commit run --all-files
```
Ruff flags 6 issues. Point out `E722` (bare `except`) and `B006` (mutable default):
real bugs, not style. `ruff check --fix .` fixes the simple ones.

**2. Tests from the spec (2 min).**
```bash
python -m pytest -q
```
4 failures: invalid percentages are accepted, and a customer with exactly 10 orders
gets no loyalty bonus (`>` instead of `>=`). *"The code runs. It just doesn't do what
we asked."*

**3. AI review (2 min).**
```bash
claude -p "Review src/shop/pricing.py against SPEC.md. Only list problems that the linter and the existing tests would NOT catch."
```
It should flag that `price_cart` overwrites prices in the caller's list, which every
test missed. If the call fails, open `fallback/ai-review.md`.
Then show `solution/test_cart_not_mutated.py`: *the AI found the gap, a test closes it.*
Key message: **AI advises, tests and gates decide.**

**4. Harness engineering (3 min).** Show `CLAUDE.md` and `.claude/settings.json`, then:
```bash
claude "Fix src/shop/pricing.py so it matches SPEC.md."
```
Watch the hooks work:
- after every edit, `guard.sh` runs lint + tests and sends failures back to Claude,
  which fixes them without you saying anything;
- if it tries to edit `tests/` or `SPEC.md`, `protect.sh` blocks it;
- it can't finish until everything is green.

No Claude? Run `./scripts/guard.sh` by hand: same checks, same message.
Reference fix: `solution/pricing.py`.

**Reset between runs:** `git checkout -- src tests`

## Intro slides (2–3, ~5 min)

1. **The problem:** AI writes code faster than we can understand it. Result: hidden
   tech debt, code nobody owns, bugs that look fine in review.
2. **Guardrails:** spec → lint → tests → AI review. Each layer catches different things.
   AI advises; deterministic checks decide.
3. **Harness engineering:** instead of only checking AI output afterwards, design the
   environment the agent works in: rules (CLAUDE.md), feedback loops (hooks that run
   tests), and limits (protected files). Better harness → better output from the same model.

## Discussion starters (~45 min)

- Which AI assistants do we use, and for what? What have they got badly wrong?
- Would our current CI have caught the `price_cart` bug?
- What would go in *our* CLAUDE.md / team rules file?
- Which files should an AI agent never touch in our repos?
- Should AI-written code get stricter checks, or the same as human code?
- One guardrail we could all adopt next week?

## Notes

- Hook behaviour (exit code 2 sends stderr back to Claude, `stop_hook_active`) follows
  the Claude Code hooks docs: https://code.claude.com/docs/en/hooks. Check them before
  the session, since Claude Code changes often.
- pre-commit uses local hooks, so nothing is downloaded during the demo.
