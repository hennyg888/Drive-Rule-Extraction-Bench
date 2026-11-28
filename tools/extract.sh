#!/usr/bin/env bash
# The draft gold-set extraction: a whole handbook, with the formal-rules prompt, on one topic, sent to
# Claude Opus 5.5 in one request. The answer is saved to
# extraction_outputs/claude-opus-5-5/<handbook>_<topic>_<YYYY_MM_DD>.json, and the whole call to
# runs/<time>-anthropic_claude-opus-5-5-<handbook>-<topic>-draft-gold/ (both at the repository root).
# It can be run from any folder:
#
#     tools/extract.sh                       # Ontario (mto), overtaking
#     tools/extract.sh tx parking            # handbook: mto, ca or tx; topic: overtaking, turning or parking
#     tools/extract.sh mto turning --dry-run # build the message and show its size, call nothing
#     tools/extract.sh ca overtaking --prompt no-image-rules       # another prompt: formal-rules (default),
#                                                                  # no-image-rules or no-handbook-rules
#     tools/extract.sh tx turning --prompt no-handbook-rules       # closed book: the region is the handbook
#                                                                  # (or pass --region mto, ca or tx)
#     tools/extract.sh mto overtaking --set effort=high            # anything after the topic goes to run_extraction.py
#
# The topic and region sentences are in drbench/prompts.py (TOPICS, REGIONS). The model settings are in
# the anthropic/claude-opus-5-5 preset in drbench/models/models.yaml.
set -euo pipefail
cd "$(dirname "$0")/.."

HANDBOOK="${1:-mto}"
shift || true
TOPIC="${1:-overtaking}"
shift || true

python tools/run_extraction.py \
    --model anthropic/claude-opus-5-5 \
    --handbook "$HANDBOOK" \
    --topic "$TOPIC" \
    --prompt formal-rules \
    --label draft-gold \
    --save-to extraction_outputs \
    "$@"
