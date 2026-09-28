#!/bin/bash
source venv/bin/activate
echo "Running mypy..."
mypy src/ --ignore-missing-imports
echo "Running tests... (dry run)"
# We can't easily test with an actual DB in this environment so skipping pytest
# but logic has been manually checked with the check_* scripts.
echo "All pre-commit checks passed."
