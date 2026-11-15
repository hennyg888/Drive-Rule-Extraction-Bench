#!/usr/bin/env bash
# The draft gold-set extraction: a whole handbook, with the formal-rules prompt, sent to Claude Opus
# 5.5 in one request. The answer is saved to extraction_outputs/<model>/<handbook>_<YYYY_MM_DD>.json,
# and the whole call to runs/<time>-anthropic_claude-opus-5-5-<handbook>-draft-gold/ (both at the
# repository root). It can be run from any folder:
#
#     tools/extract.sh                       # Ontario (mto)
#     tools/extract.sh tx                    # another handbook: mto, ca or tx
#     tools/extract.sh mto --dry-run         # count the input tokens (free), call nothing
#     tools/extract.sh mto --set effort=high # anything after the handbook goes to run_extraction.py
#
# The model settings (effort medium, 128K output tokens) are in the preset in drbench/models/models.yaml.
set -euo pipefail
cd "$(dirname "$0")/.."

HANDBOOK="${1:-mto}"
shift || true

python tools/run_extraction.py \
    --model anthropic/claude-opus-5-5 \
    --handbook "$HANDBOOK" \
    --prompt formal-rules \
    --label draft-gold \
    --save-to extraction_outputs \
    "$@"
