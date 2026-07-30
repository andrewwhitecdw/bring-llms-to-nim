#!/bin/bash
set -e
WORKFLOW=".github/workflows/ci.yml"

if grep -q 'run_notebook "deploy/2_TRTLLM_Checkpoints_Engines.ipynb" "fix_trtllm_path"' "$WORKFLOW"; then
    echo "FAIL: run_notebook still receives unused second argument"
    exit 1
fi

