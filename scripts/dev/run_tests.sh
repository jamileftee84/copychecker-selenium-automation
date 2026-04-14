#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT_DIR"

run_module() {
  local file_path="$1"
  local module
  module="${file_path#./}"
  module="${module%.py}"
  module="${module//\//.}"
  python -m "$module"
}

if [[ $# -gt 0 ]]; then
  run_module "$1"
  exit 0
fi

for test_file in tools/automation/tests/test_*.py; do
  echo "Running ${test_file}"
  run_module "$test_file"
done
