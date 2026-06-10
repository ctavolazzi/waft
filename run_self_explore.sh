#!/usr/bin/env bash
# Launch the Self-Explorer stack: Gemma4 brain + Waft API + Dashboard
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LLAMA_SERVER="$HOME/Code/llama.cpp/build/bin/llama-server"
MODEL="$HOME/google_gemma-4-E4B-it-Q4_K_M.gguf"

echo "=== Self-Explorer Stack ==="
echo "  BRAIN:  llama-server on :8080"
echo "  WAFT:   waft serve on :8000"
echo "  DASH:   dashboard on :5050 (served by waft)"
echo ""

npx concurrently \
  --names "BRAIN,WAFT" \
  --prefix-colors "magenta,cyan" \
  "$LLAMA_SERVER -m $MODEL --port 8080 -ngl 0" \
  "cd $SCRIPT_DIR && waft dashboard-5050 --port 5050 --path $SCRIPT_DIR"
