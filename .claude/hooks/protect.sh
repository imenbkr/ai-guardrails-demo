#!/usr/bin/env bash
# Claude Code PreToolUse hook: the agent may not edit the tests or the spec.
# Otherwise the easiest way to "make the tests pass" is to change the tests.
input="$(cat)"
path=$(printf '%s' "$input" | python3 -c 'import json,sys
try: print(json.load(sys.stdin).get("tool_input", {}).get("file_path", ""))
except Exception: print("")')
case "$path" in
  */tests/*|tests/*|*SPEC.md|*/.claude/*|.claude/*)
    echo "Blocked by harness: $path is protected. Tests and SPEC.md are the source of truth; change the code instead." >&2
    exit 2 ;;
esac
exit 0
