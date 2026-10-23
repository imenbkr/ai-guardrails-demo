#!/usr/bin/env bash
# The same checks the AI agent gets, runnable by hand. Works without Claude.
set -u
cd "$(dirname "$0")/.."
status=0
echo "== pre-commit (lint + format) =="
pre-commit run --all-files || status=1
echo
echo "== pytest (spec acceptance tests) =="
python -m pytest -q || status=1
echo
if [ $status -eq 0 ]; then echo "GUARD: all checks passed"; else echo "GUARD: checks failed"; fi
exit $status
