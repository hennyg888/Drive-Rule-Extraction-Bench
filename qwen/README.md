# Qwen trial: running the extraction (T2) with open models

Trial design, sampling settings and model choices are in `../qwen-trial-handoff.md`. This folder holds the scripts. The prompt lives in `../prompts/`.

## What is where

| Path | What it is |
|---|---|
| `prompts/extract-rules.md` | The prompt (v2): the task, why the rules are extracted (how a driving VLA uses them), the rule language, the output, the extraction steps and a final check. It states general principles and holds no topic- or case-specific rules |
| `analysis/rule-language-v1.md` | The rule language (frozen). The prompt describes it in its own words and copies its grammar block verbatim |
| `prompts/topics/passing.md` | The topic, as one paragraph |
| `prompts/examples/extract-examples.json` | 8 worked examples from outside the passing topic, so none is scored. Each shows the reading notes, then the statements |
| `prompts/archive/` | v1 of the prompt, topic and examples (case-based, with the spec pasted in) |
| `qwen/build_prompt.py` | Builds the system prompt and one user message per handbook page. `PROMPT_VERSION` names the prompt |
| `qwen/run_extract.py` | Sends the batches to a vLLM server, saves everything, merges and checks |
| `qwen/score_t2.py`, `qwen/compare_t2.py` | Score a run against the reference; write a side-by-side comparison |
| `tools/check_statements.py` | Checks any statements file: schema, keywords, force, clauses, flags, quotes, numbers, links, and that every passage the model noted as about the topic is cited |

The model answers with **reading notes** first (`passages`: one entry per input passage, saying whether it is about the topic and what it says), then the statements. The notes make the model account for every passage before writing, which is the main guard against missed content, and let the checker find passages it noted but never used. The statements themselves follow the frozen schema (`analysis/passing-rules/statements.schema.json`).

To change the prompt, edit `prompts/extract-rules.md`, the topic or the examples, then rerun. Every run saves the exact system prompt it used.

## This server

- 4 × RTX 4090, 24 GB each. CUDA driver 13.4.
- vLLM 0.32.0 is installed in `~/qwen-trial/.venv` (torch 2.13 + CUDA 13.2, xgrammar 0.2.8).
- Weights are in `~/hf` (`/data` is read-only for this account). Downloaded: Qwen3.5-0.8B, 2B, 4B, 9B, Qwen3.5-27B-FP8 and Qwen3.8-27B-FP8. BF16 27B would need all four GPUs; FP8 fits on two.
- The GPUs are shared. Check `nvidia-smi` before starting a server.

## Run

In one shell, start a server. One model at a time; the smallest first.

```bash
cd ~/qwen-trial && source .venv/bin/activate && export HF_HOME=$HOME/hf
CUDA_VISIBLE_DEVICES=0 vllm serve Qwen/Qwen3.5-0.8B --served-model-name qwen3.5-0.8b \
  --language-model-only --reasoning-parser qwen3 --max-model-len 65536 \
  --gpu-memory-utilization 0.90 --port 8000
```

| Model | GPUs | Extra flags |
|---|---|---|
| Qwen3.5-0.8B, 2B, 4B | `CUDA_VISIBLE_DEVICES=0` | |
| Qwen3.5-9B | `CUDA_VISIBLE_DEVICES=0,1` | `--tensor-parallel-size 2` (18 GB of weights leaves little KV cache on one 24 GB card) |
| Qwen3.5-27B-FP8, Qwen3.8-27B-FP8 | `CUDA_VISIBLE_DEVICES=0,1` | `--tensor-parallel-size 2` |

In a second shell, from the repo root:

```bash
source ~/qwen-trial/.venv/bin/activate
python qwen/run_extract.py --model qwen3.5-0.8b --handbook mto --seed 1                 # thinking off
python qwen/run_extract.py --model qwen3.5-0.8b --handbook mto --seed 1 --thinking      # thinking on
python qwen/run_extract.py --model qwen3.5-0.8b --batch "Stopping"                      # one page only, for a quick look
```

Output goes to `runs/t2/<handbook>/<model>/<prompt version>/<think|nothink>/seed<k>/`: the system prompt, one JSON per page (prompt, raw answer, thinking, usage, parsed answer), the merged `statements.json` (reading notes and statements) and `check.txt`. Statement ids get a page prefix (`p03:s4`) because each page is numbered independently.

Then score and compare:

```bash
python qwen/score_t2.py runs/t2/mto/<model>/v2/think/seed1/statements.json
python qwen/compare_t2.py runs/t2/mto/<model>/v2/think/seed1/statements.json --out compare.md
```

`score_t2.py` reports statement recall and precision; agreement on type, force, modal and force basis; vague-word span F1; statements written from excluded passages; passage and sentence recall (how much of the handbook text the reference uses is also used by the model); and the hard-case subsets. Add `--only-seen` when the run covered only some pages (`--batch`).

The prompt is about 13k tokens, and a page batch adds up to 9k tokens. 65,536 tokens of context leaves room for 16k output tokens and thinking.

## Iterating on the prompt

1. Run one model on one page, `--batch "Stopping"` for example, and read `check.txt` and the raw answers.
2. Find the failures that repeat (a missing heading condition, a wrong force basis, quotes not verbatim) and fix the method step that should prevent them. Add an example only when a step cannot say it clearly. Examples must come from outside the passing topic, so they never show a scored answer.
3. Rerun the same page with the same seed and compare.

The v1 spec quotes 10 reference statements, whole or in part, in its own examples: 1b, 3.1.1a, 3.1.3a, 3.2.3a, 3.2.3b, 3.2.4a, 3.4.3a, 3.4.5a, 3.4.6c and 3.5.2c. Report those separately when scoring T2, since the model has seen them. The method, topic and examples in `prompts/` quote no reference statement and no scored passage; keep it that way when editing them.
