# Candidate model runs: Ontario overtaking

This page records the extraction runs of 22 and 23 November 2026. Seven models were given the Ontario
(MTO) driver's handbook and asked for its overtaking rules, with the same prompt as the Claude draft
behind the gold set. Twelve results are stored here, one per model and thinking mode.

## Summary

- **The hosted GPT-6.2 models cover the most.** Their rules cite 108 to 117 of the 126 handbook blocks the gold set cites. The best local run cites 54.
- **Qwen3.8-27B with thinking is the strongest local model:** 65 rules in 17.6 minutes.
- **The other local models find far fewer rules:** 22 to 30 for Muse Glimmer 30B and Gemma 4 31B, 10 to 13 for MiniCPM-V 4.7 and GLM-4.6V-Flash.
- **Thinking helped Qwen and Gemma and hurt GLM.** Qwen went from 40 to 65 rules and Gemma from 22 to 30. GLM went from 13 to 10, and 7 of those 10 cite no block the gold set uses.
- **Cost:** the local runs have no fee. The four OpenAI runs cost $3.82 together.
- **Reproducibility:** every local result came out byte for byte the same in a repeat run. The OpenAI runs were not repeated.

All numbers on this page are counts: how many rules, and which handbook blocks they cite. They do not
say whether a rule means the same as a gold rule. That comparison (Part B of
[`goldset_check_pipeline_plan.md`](../goldset_check_pipeline_plan.md)) is not built yet.

## What every run got

- **Handbook:** MTO, all 30 pages in one request: 414,664 characters of HTML, 245 images (JPEG, sent in their place in the text) and the table of contents.
- **Prompt:** [`prompts/formal-rules`](../prompts/formal-rules) (`system.md`, `task.md`, `schema.json`), SHA-256 `3e330fa2b145…`, unchanged from the Claude draft runs.
- **Answer format:** one JSON object (scope, vocabulary, rules), enforced by the server with the JSON schema.
- **Topic:** overtaking, as set in `task.md`.

## Models

| Model | Where it ran | Version | Parameters | Thinking switch |
|---|---|---|---:|---|
| GPT-6.2 Astra | OpenAI API | `gpt-6.2-astra` | not published | `reasoning_effort` (API default medium) |
| GPT-6.2 Sol | OpenAI API | `gpt-6.2-sol` | not published | `reasoning_effort` (API default medium) |
| Qwen3.8-27B | local | `Qwen/Qwen3.8-27B` at `37561816` | 27.78 B | `enable_thinking`, on by default at effort xhigh |
| Muse Glimmer 30B | local | `meta-models/Muse-Glimmer-30B` at `1297fd7d` | 29.78 B | `reasoning_strength`, default high |
| Gemma 4 31B | local | `google/gemma-4-31B-it` at `842da379` | 31.27 B | `enable_thinking`, off by default |
| MiniCPM-V 4.7 35B-A3B | local | `openbmb/MiniCPM-V-4.7-35B-A3B` at `98e79ba9` | 35.21 B | `enable_thinking`, off by default |
| GLM-4.6V-Flash | local | `zai-org/GLM-4.6V-Flash` at `411bb4d7` | 10.29 B | `enable_thinking`, on by default |

The local versions are Hugging Face repositories and the first eight characters of the pinned
revision; the full revision is in each preset in
[`drbench/models/models.yaml`](../drbench/models/models.yaml). Parameter counts are read from the
weight files. MiniCPM-V is a mixture-of-experts model, so only part of its 35 B parameters is used
for each token.

## Results

| Model and mode | Rules | Vocabulary terms | Blocks cited | Of these, in the gold set | Rules citing no gold block | Format errors |
|---|---:|---:|---:|---:|---:|---:|
| GPT-6.2 Astra, effort high | 83 | 17 | 213 | 117 | 14 | 3 |
| GPT-6.2 Astra, effort medium | 59 | 12 | 162 | 116 | 5 | 6 |
| GPT-6.2 Sol, effort high | 75 | 12 | 175 | 115 | 12 | 12 |
| GPT-6.2 Sol, effort medium | 77 | 10 | 160 | 108 | 8 | 9 |
| Qwen3.8-27B, thinking | 65 | 11 | 55 | 54 | 0 | 4 |
| Qwen3.8-27B, no thinking | 40 | 12 | 31 | 28 | 3 | 5 |
| Muse Glimmer 30B, reasoning high | 30 | 9 | 23 | 22 | 1 | 2 |
| Gemma 4 31B, thinking (sampled) | 30 | 6 | 24 | 20 | 4 | 2 |
| Gemma 4 31B, no thinking | 22 | 4 | 14 | 14 | 0 | 4 |
| MiniCPM-V 4.7 35B-A3B, no thinking | 11 | 9 | 17 | 12 | 4 | 7 |
| GLM-4.6V-Flash, no thinking | 13 | 3 | 11 | 9 | 2 | 7 |
| GLM-4.6V-Flash, thinking | 10 | 5 | 10 | 3 | 7 | 13 |
| *Claude Opus 5.5 raw draft (14 Nov, for reference)* | 68 | 19 | 85 | 80 | 0 | 5 |
| *Gold set* | 77 | 22 | 126 | 126 | 0 | 0 |

- **Blocks cited** counts the distinct handbook blocks (ids such as `10.15`) in the `evidence` of the rules.
- **In the gold set** counts those that the gold set's rules also cite. The gold set cites 126.
- **Rules citing no gold block** are rules whose evidence lies wholly outside what the gold set uses. They are either off topic or rules the gold set left out; the counts cannot tell which.
- **Format errors** come from stage 1 of the gold-set check, [`check_format.py`](../error_check_pipelines/goldset/check_format.py).

### Rules by force

| Model and mode | Rules | Requirement | Instruction | Advice | Permission |
|---|---:|---:|---:|---:|---:|
| GPT-6.2 Astra, effort high | 83 | 23 | 50 | 5 | 5 |
| GPT-6.2 Astra, effort medium | 59 | 16 | 37 | 2 | 4 |
| GPT-6.2 Sol, effort high | 75 | 19 | 48 | 4 | 4 |
| GPT-6.2 Sol, effort medium | 77 | 22 | 44 | 7 | 4 |
| Qwen3.8-27B, thinking | 65 | 11 | 44 | 6 | 4 |
| Qwen3.8-27B, no thinking | 40 | 12 | 21 | 3 | 4 |
| Muse Glimmer 30B, reasoning high | 30 | 14 | 10 | 3 | 3 |
| Gemma 4 31B, thinking (sampled) | 30 | 19 | 0 | 7 | 4 |
| Gemma 4 31B, no thinking | 22 | 8 | 10 | 2 | 2 |
| MiniCPM-V 4.7 35B-A3B, no thinking | 11 | 9 | 1 | 0 | 1 |
| GLM-4.6V-Flash, no thinking | 13 | 5 | 2 | 5 | 1 |
| GLM-4.6V-Flash, thinking | 10 | 5 | 1 | 2 | 2 |
| *Claude Opus 5.5 raw draft (14 Nov, for reference)* | 68 | 13 | 43 | 9 | 3 |
| *Gold set* | 77 | 18 | 48 | 6 | 5 |

Gemma with thinking gave no rule the force `INSTRUCTION`, which is the largest class in the gold set.

### Rules by group

Each model chooses its own group codes, so the same code may not cover the same rules. The columns
are the gold set's groups: GEN general, PROC how to pass, NIGHT at night, LOC places, MARK lane
markings, SIGN signs, SIDE which side, USER particular road users, WX weather, BEING being passed,
TOW towing.

| Model and mode | GEN | PROC | NIGHT | LOC | MARK | SIGN | SIDE | USER | WX | BEING | TOW | Other groups |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| GPT-6.2 Astra, effort high | 3 | 11 |  | 10 |  |  | 4 | 7 | 5 | 10 | 4 | LANE 7, BIKE 6, BUS 7, LIGHT 2, WORK 7 |
| GPT-6.2 Astra, effort medium | 2 | 6 |  | 8 | 2 |  | 10 | 20 | 3 | 5 | 3 | none |
| GPT-6.2 Sol, effort high |  | 12 |  | 14 | 2 |  | 4 | 18 |  | 8 | 4 | LANE 5, BUS 5, CAR 3 |
| GPT-6.2 Sol, effort medium | 2 | 6 |  | 6 | 2 |  | 4 | 12 |  | 4 | 5 | LANE 7, BIKE 7, BUS 4, TRAM 3, HAZ 15 |
| Qwen3.8-27B, thinking | 7 | 6 | 3 | 9 | 2 |  | 3 | 15 |  | 10 | 3 | SHLD 2, TRAM 3, CLIMB 2 |
| Qwen3.8-27B, no thinking | 2 | 9 |  | 6 | 2 |  | 3 | 10 |  | 5 | 3 | none |
| Muse Glimmer 30B, reasoning high | 11 |  | 3 | 3 | 2 |  | 4 | 7 |  |  |  | none |
| Gemma 4 31B, thinking (sampled) | 2 | 6 | 4 | 3 |  |  | 4 | 9 |  | 2 |  | none |
| Gemma 4 31B, no thinking | 2 | 5 | 3 | 3 |  |  | 4 | 2 |  | 3 |  | none |
| MiniCPM-V 4.7 35B-A3B, no thinking |  | 1 |  | 3 | 2 |  |  | 4 |  | 1 |  | none |
| GLM-4.6V-Flash, no thinking |  | 3 |  | 3 |  |  | 3 | 2 |  | 2 |  | none |
| GLM-4.6V-Flash, thinking | 1 |  | 1 |  |  |  | 2 | 2 |  |  |  | SPACE 1, SHORE 1, PASSED 1, HOV 1 |
| *Claude Opus 5.5 raw draft (14 Nov, for reference)* | 6 | 7 | 4 | 7 | 2 | 5 | 3 | 21 | 3 | 6 | 4 | none |
| *Gold set* | 7 | 7 | 4 | 8 | 2 | 5 | 5 | 25 | 3 | 7 | 4 | none |

### Evidence by kind of block

Each cell counts citations, so a block cited by two rules counts twice.

| Model and mode | Text | Figure | Figure caption | Heading | No such block |
|---|---:|---:|---:|---:|---:|
| GPT-6.2 Astra, effort high | 255 | 50 | 15 | 16 | 0 |
| GPT-6.2 Astra, effort medium | 160 | 36 | 11 | 7 | 0 |
| GPT-6.2 Sol, effort high | 198 | 44 | 16 | 7 | 0 |
| GPT-6.2 Sol, effort medium | 182 | 42 | 14 | 4 | 0 |
| Qwen3.8-27B, thinking | 77 | 10 | 5 | 0 | 0 |
| Qwen3.8-27B, no thinking | 46 | 2 | 0 | 0 | 0 |
| Muse Glimmer 30B, reasoning high | 34 | 1 | 0 | 0 | 0 |
| Gemma 4 31B, thinking (sampled) | 34 | 0 | 0 | 4 | 0 |
| Gemma 4 31B, no thinking | 27 | 1 | 0 | 0 | 0 |
| MiniCPM-V 4.7 35B-A3B, no thinking | 18 | 3 | 0 | 4 | 1 |
| GLM-4.6V-Flash, no thinking | 13 | 1 | 0 | 3 | 0 |
| GLM-4.6V-Flash, thinking | 7 | 1 | 0 | 7 | 0 |

The GPT-6.2 models cite 36 to 50 figures per run. No local model cites more than 10, and Gemma with
thinking cites none. MiniCPM-V cited one block id that does not exist.

### Format errors by check

Checks 1 (schema), 4 (force and modal) and 5 (evidence) found nothing in any result.

| Model and mode | Statement matches fields | Ids and numbering | Vague terms | Vocabulary | Lowercase vocab terms | Total |
|---|---:|---:|---:|---:|---:|---:|
| GPT-6.2 Astra, effort high |  |  |  |  | 3 | 3 |
| GPT-6.2 Astra, effort medium |  |  |  | 2 | 4 | 6 |
| GPT-6.2 Sol, effort high |  |  |  |  | 12 | 12 |
| GPT-6.2 Sol, effort medium |  |  |  | 1 | 8 | 9 |
| Qwen3.8-27B, thinking | 1 |  |  | 2 | 1 | 4 |
| Qwen3.8-27B, no thinking |  |  |  | 3 | 2 | 5 |
| Muse Glimmer 30B, reasoning high | 1 |  |  |  | 1 | 2 |
| Gemma 4 31B, thinking (sampled) |  |  |  | 2 |  | 2 |
| Gemma 4 31B, no thinking | 2 |  |  | 2 |  | 4 |
| MiniCPM-V 4.7 35B-A3B, no thinking | 3 |  |  | 3 | 1 | 7 |
| GLM-4.6V-Flash, no thinking | 4 |  |  | 3 |  | 7 |
| GLM-4.6V-Flash, thinking | 3 | 2 | 1 | 6 | 1 | 13 |
| *Claude Opus 5.5 raw draft (14 Nov, for reference)* |  |  |  | 2 | 3 | 5 |
| *Gold set* |  |  |  |  |  | 0 |

## Tokens, time and cost

| Model and mode | Input tokens | Output tokens | Of which reasoning | Output limit | Time | Cost |
|---|---:|---:|---:|---:|---:|---:|
| GPT-6.2 Astra, effort high | 114,518 | 19,087 | 2,912 | 128,000 | 4.7 min | $1.68 |
| GPT-6.2 Astra, effort medium | 114,518 | 10,755 | 34 | 128,000 | 2.2 min | $1.35 |
| GPT-6.2 Sol, effort high | 114,518 | 18,526 | 2,924 | 128,000 | 3.8 min | $0.41 |
| GPT-6.2 Sol, effort medium | 114,518 | 14,757 | 357 | 128,000 | 2.8 min | $0.38 |
| Qwen3.8-27B, thinking | 132,489 | 45,948 | 32,928 | 100,000 | 17.6 min | no fee |
| Qwen3.8-27B, no thinking | 132,453 | 9,495 | 0 | 100,000 | 4.8 min | no fee |
| Muse Glimmer 30B, reasoning high | 114,242 | 17,854 | not reported | 75,000 | 12.3 min | no fee |
| Gemma 4 31B, thinking (sampled) | 180,754 | 9,827 | 3,274 | 58,000 | 8.6 min | no fee |
| Gemma 4 31B, no thinking | 180,756 | 3,700 | 0 | 32,000 | 5.1 min | no fee |
| MiniCPM-V 4.7 35B-A3B, no thinking | 131,563 | 3,052 | 0 | 32,000 | 0.8 min | no fee |
| GLM-4.6V-Flash, no thinking | 114,019 | 2,773 | 0 | 16,900 | 1.2 min | no fee |
| GLM-4.6V-Flash, thinking | 114,015 | 4,519 | 2,188 | 16,900 | 1.5 min | no fee |

- **Input tokens differ for the same request** because each model has its own tokenizer and its own cost per image. Gemma spends 280 tokens on every image, which is 68,600 of its 180,754.
- **Every run stopped by itself**, not at the output limit.
- **Muse's reasoning tokens** are not counted separately by the server. Its reasoning text is 50,060 characters.
- **GPT-6.2 barely reasoned.** At effort medium Astra spent 34 reasoning tokens and Sol 357; at high each spent about 2,900. Qwen spent 32,928.
- **Local runs** have no fee. The eight stored runs took 52 minutes in total on the four GPUs. Each was also repeated at least once, and loading a model takes a few more minutes.
- **OpenAI costs** are the token counts times the list prices per million tokens: Sol $2 input and $10 output, Astra $8 and $40. They are not read from the bill.

## Inference details

### Local models (vLLM)

- **Machine:** 4 × NVIDIA RTX 4090 (24 GB each), AMD Threadripper PRO 3955WX, 123 GiB of RAM. The GPUs are shared with other users.
- **Software:** vLLM 0.32.0, PyTorch 2.13.0 with CUDA 13.2, Transformers 5.19.0.
- **Weights:** full precision (BF16), no quantized build.
- **Serving:** one model at a time, split over the four GPUs (`--tensor-parallel-size 4`), behind vLLM's OpenAI-compatible API on localhost.
- **Decoding:** greedy (`temperature: 0`), not the sampling settings on the model cards, so that a fixed prompt gives one answer.
- **One exception:** Gemma with thinking loops under greedy decoding. It uses its card's sampling (temperature 1.0, top_p 0.95, top_k 64) with seed 0.
- **Settings needed for the same answer twice:** `--max-num-seqs 1`, `--no-enable-prefix-caching`, `--seed 0`, and a reset of vLLM's image-embedding cache before every request (`POST /reset_encoder_cache`, which needs `VLLM_SERVER_DEV_MODE=1`). Without the reset, two greedy Qwen runs gave 65 and 68 rules.

| Model | Context served | Reasoning parser | Note |
|---|---:|---|---|
| Qwen3.8-27B | 262,144 | `qwen3` | the model's full context |
| Muse Glimmer 30B | 196,608 | `muse_glimmer` | the card says 131,072; raised with `--hf-overrides` because input and output together were 132,096 |
| Gemma 4 31B | 240,000 | `gemma4` | the model's 262,144 does not fit beside the weights |
| MiniCPM-V 4.7 35B-A3B | 262,144 | `minicpmv` | no-thinking mode only |
| GLM-4.6V-Flash | 131,072 | `glm45` | the model's full context |

The full start command of each server is the `serve` line of its preset, and is copied into every
run's `.meta.json`.

### OpenAI models

- **API:** Chat Completions, one request per run, with the `openai` Python SDK 3.41.0.
- **Settings:** `reasoning_effort` medium or high, `max_completion_tokens` 128,000, the JSON schema in strict mode.
- **No decoding control:** these models accept no temperature or top_p, so a repeat may differ.
- **Images:** sent as they are, at the API's default detail.

### Reproducibility checks

| Model and mode | Runs of the same request | Outcome |
|---|---|---|
| Qwen3.8-27B, thinking | 3, one after a server restart | identical |
| Qwen3.8-27B, no thinking | 2 | identical |
| Gemma 4 31B, thinking (sampled, seed 0) | 3 | identical |
| Gemma 4 31B, no thinking | 2 | identical |
| Muse Glimmer 30B, reasoning high | 2 | identical |
| MiniCPM-V 4.7 35B-A3B, no thinking | 2 | identical |
| GLM-4.6V-Flash, both modes | 2 each | identical |
| GPT-6.2 Astra and Sol | 1 each | not checked |

## Model size and memory

| Model | Parameters | Weights on disk | GPU memory after loading, per GPU | Left for the KV cache, per GPU | KV cache holds |
|---|---:|---:|---:|---:|---:|
| Qwen3.8-27B | 27.78 B | 55.6 GB | 13.02 GiB | 8.19 GiB | 530,492 tokens |
| Muse Glimmer 30B | 29.78 B | 59.6 GB | 16.44 GiB | 4.44 GiB | 654,043 tokens |
| Gemma 4 31B | 31.27 B | 62.5 GB | 16.06 GiB | 5.90 GiB | 247,237 tokens |
| MiniCPM-V 4.7 35B-A3B | 35.21 B | 70.4 GB | 16.67 GiB | 2.64 GiB | 275,698 tokens |
| GLM-4.6V-Flash | 10.29 B | 20.6 GB | 5.03 GiB | 9.17 GiB | 480,912 tokens |

- **Source:** the memory figures are what vLLM logged at start. GPU memory was not sampled during the runs.
- **What `nvidia-smi` shows:** vLLM reserves 95% of every card at start (`--gpu-memory-utilization 0.95`, about 22.8 GiB of 24), so all four cards look nearly full for every model, also the small one.
- **The KV cache is the limit on context.** Gemma needs 6.15 GiB per GPU for its full 262,144 tokens and had 5.8, which is why it is served with 240,000.
- **Disk:** the five sets of weights take 269 GB.
- **The OpenAI models** are hosted, so their size and memory are not known.

## Runs that gave no stored result

- **Qwen3.8-27B, first greedy runs:** two runs of the same request gave 65 and 68 rules. This led to the cache reset above; the stored result is from after it.
- **Gemma 4 31B, thinking, greedy:** it repeated one block of reasoning 32 times until the 58,000-token output limit and gave no answer. The stored thinking result uses seeded sampling.
- **Gemma 4 31B at 262,144 context:** the server did not start (see the KV cache note above).
- **Muse Glimmer 30B at its stated 131,072 context:** the request did not fit.
- **MiniCPM-V 4.7, thinking:** it wrote a 12-rule answer in the reasoning channel and stopped, so there was no final answer.

## Where things are

In this folder, each result is at `<vendor>/<model>/<mode>/<handbook>_<date>.json`:

```
anthropic/
  claude-opus-5.5/
    mto_2026_11_14.json
    tx_2026_11_21.json
google/
  gemma-4-31b-it/
    no-thinking/              mto_2026_11_23.json
    thinking-sampled-seed0/   mto_2026_11_23.json
meta/
  muse-glimmer-30b/
    reasoning-high/           mto_2026_11_23.json
openai/
  gpt-6.2-astra/
    reasoning-high/           mto_2026_11_23.json
    reasoning-medium/         mto_2026_11_23.json
  gpt-6.2-sol/
    reasoning-high/           mto_2026_11_23.json
    reasoning-medium/         mto_2026_11_23.json
openbmb/
  minicpm-v-4.7-35b-a3b/
    no-thinking/              mto_2026_11_23.json
qwen/
  qwen3.8-27b/
    no-thinking/              mto_2026_11_22.json
    thinking-xhigh/           mto_2026_11_22.json
z-ai/
  glm-4.6v-flash/
    no-thinking/              mto_2026_11_23.json
    thinking/                 mto_2026_11_23.json
```

- **`<handbook>_<date>.json`** is the model's answer.
- **`<handbook>_<date>.meta.json`** next to it records the preset, the model, every setting, the server's start command (local models), the prompt's SHA-256, the token counts, the time and the cost.
- **The two Claude Opus 5.5 files** are the earlier raw drafts behind the gold sets. They predate the mode folders and have no `.meta.json`.

Elsewhere:

- **Presets:** [`drbench/models/models.yaml`](../drbench/models/models.yaml), sections "OpenAI API" and "local vLLM". Its comments record what was measured for each model.
- **Full run folders:** `runs/<time>-<preset>-mto…/` at the repository root, with the request as text, the raw response, the reasoning text and `grounded.json`. `runs/` is not in git, so these exist only on the server the runs were made on.
- **Gold set:** [`gold_set/mto/overtaking/gold_set.json`](../gold_set/mto/overtaking/gold_set.json).
- **On the server, outside the repository:** weights in `~/hf`, vLLM in `~/qwen-trial/.venv`, server and run logs in `~/qwen-trial/logs/`.

To repeat a run and check it:

```
python tools/models.py serve local/qwen3.8-27b          # local models only; stop it when done
python tools/run_extraction.py --model local/qwen3.8-27b --handbook mto --save-to extraction_outputs
python tools/run_extraction.py --model openai/gpt-6.2-sol --handbook mto --save-to extraction_outputs/openai
python error_check_pipelines/goldset/check_format.py <answer.json> --handbook mto
```

The OpenAI presets name the model without a vendor, so they are saved with
`--save-to extraction_outputs/openai`. They need `OPENAI_API_KEY` in `.env`.

## Limits of these runs

- **Counts, not meaning.** See the note under the summary.
- **One handbook.** Only MTO was run; the Texas gold set exists and was not used.
- **Thinking is not matched across models.** Qwen ran at its default effort, the GPT-6.2 models reasoned very little at either setting, and the Claude draft used effort medium.
- **Gemma's thinking result is sampled**, with a fixed seed; all other local results are greedy.
- **The OpenAI results are single runs.**
