# Project rules for AI agents (the "harness")

Claude Code reads this file automatically. It turns team conventions into
instructions the agent follows on every task.

## Source of truth
- `SPEC.md` defines the expected behaviour. If code and spec disagree, the spec wins.
- Never edit `SPEC.md` or anything in `tests/`. If a test looks wrong, stop and say so.

## Code rules
- No bare `except:` and never silently swallow errors. Invalid input raises an error.
- Functions must not change the objects passed to them.
- No mutable default arguments.
- Remove unused imports. Keep functions short and readable.

## Definition of done
- `./scripts/guard.sh` passes (lint, format and all tests).
- Explain in 2–3 bullet points what you changed and why.
