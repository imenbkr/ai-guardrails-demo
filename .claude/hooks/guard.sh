#!/usr/bin/env bash
# Claude Code hook: runs lint + tests after every AI edit (PostToolUse)
# and before the AI says it is done (Stop).
# Exit code 2 = send the failure back to Claude so it fixes it itself.
cd "${CLAUDE_PROJECT_DIR:-$(dirname "$0")/../..}" || exit 0
[ -x .venv/bin/python ] && export PATH="$PWD/.venv/bin:$PATH"
input="$(cat)"

# Stop hook: avoid an endless loop if Claude is already retrying after a Stop block.
if [ "${1:-}" = "--stop" ]; then
  active=$(printf '%s' "$input" | python3 -c 'import json,sys
try: print(json.load(sys.stdin).get("stop_hook_active", False))
except Exception: print(False)')
  [ "$active" = "True" ] && exit 0
fi

lint=$(ruff check --output-format concise . 2>&1); lint_rc=$?
tests=$(python -m pytest -q --tb=line 2>&1); test_rc=$?

if [ $lint_rc -ne 0 ] || [ $test_rc -ne 0 ]; then
  {
    echo "Guardrails failed. Fix the code (not the tests, not SPEC.md) and try again."
    [ $lint_rc -ne 0 ] && { echo "--- ruff ---"; echo "$lint" | tail -40; }
    [ $test_rc -ne 0 ] && { echo "--- pytest ---"; echo "$tests" | tail -25; }
  } >&2
  exit 2
fi
exit 0
