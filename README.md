# Drive-Rule-Extract-Bench

This is a dataset and framework for benchmarking how well visual language models (VLMs) can extract formalized rules of the road from a driver's handbook. It tests for accuracy, coverage, and correct attribution to source materials as input modalities vary (E.g. text-only, text-and-image, whole page as image). 

Project for VLM CS886 F26 by Michael Lee and Henry Guo.

## Handbooks

The three handbooks are kept as local HTML pages with their images. These HTML copies are the source of truth: everything given to a model is built from them, in their page order with the images where they appear. Each handbook folder also keeps the published PDF, for people to read; the PDFs are not used as model input for now.

| Handbook | HTML pages and images | PDF | Made by |
|---|---|---|---|
| Official MTO Driver's Handbook (Ontario) | `handbooks/mto/`: 30 pages, 241 images | `handbooks/mto/source/MTO-drivers-handbook-ontario.ca.pdf` | `scrapers/scrape_mto_handbook.py`, from the ontario.ca web pages |
| California Driver's Handbook, DL 600 (Rev. 6/2025) | `handbooks/ca/`: 23 pages, 74 images | `handbooks/ca/source/DL-600.pdf` | `scrapers/scrape_ca_handbook.py`, from the dmv.ca.gov web pages |
| Texas Driver Handbook, DL-7 (revised January 2026) | `handbooks/tx/`: 21 pages, 203 images | `handbooks/tx/source/DL-7.pdf` | `scrapers/scrape_tx_handbook.py`, from the DPS PDF (Texas publishes no web version) |

The handbooks are state- and province-wide: San Francisco and Austin drivers use the California and Texas handbooks.

All three HTML copies have the same layout, so one program can read any of them. The handbook text is inside `<article class="content">`, with headings, lists and tables as ordinary HTML and every image in the folder's `images/`. Open `index.html` in each folder to browse it.

## Handbook analysis

What each handbook gives a model: the text and images inside the pages' `<article class="content">`. A text block is a paragraph, a list item or a table row.

| | Ontario (MTO) | California (DMV) | Texas (DPS) |
|---|---:|---:|---:|
| Pages | 30 | 23 | 21 |
| Headings | 454 | 229 | 295 |
| Text blocks (paragraphs, list items, table rows) | 1,911 | 1,023 | 1,788 |
| Sentences | 3,587 | 1,695 | 2,711 |
| Words | 53,789 | 21,463 | 41,814 |
| Text tokens | 66,692 | 27,563 | 53,935 |
| Words per block: median / 90th percentile / max | 18 / 63 / 195 | 14 / 41 / 207 | 16.5 / 49 / 222 |
| Blocks with more than 3 sentences | 218 | 74 | 81 |
| Blocks with more than 80 words | 77 | 15 | 40 |
| Images (distinct files) | 245 (241) | 74 (74) | 203 (203) |
| Image median size (px) | 170 x 104 | 228 x 198 | 138 x 138 |
| Image pixels (millions) | 7.4 | 5.7 | 10.3 |
| Image tokens (estimate) | 9,310 | 7,213 | 13,254 |

Text tokens counted with the Qwen/Qwen3.8-27B-FP8 tokenizer. Image tokens estimated as one per 28 x 28 pixel patch, as Qwen-VL models encode images; other models differ (Claude: about width x height / 750).

<details><summary>Ontario (MTO): per page</summary>

| Page | Words | Text tokens | Images | Image tokens |
|---|---:|---:|---:|---:|
| `index` | 382 | 482 | 0 | 0 |
| `getting-your-drivers-licence` | 4,619 | 6,088 | 10 | 174 |
| `safe-and-responsible-driving` | 466 | 554 | 0 | 0 |
| `getting-ready-drive` | 3,009 | 3,609 | 7 | 210 |
| `driving-along` | 976 | 1,156 | 2 | 178 |
| `sharing-road-other-road-users` | 2,661 | 3,259 | 10 | 1,432 |
| `driving-through-intersections` | 668 | 862 | 7 | 284 |
| `stopping` | 1,224 | 1,481 | 7 | 506 |
| `changing-directions` | 2,276 | 2,848 | 15 | 544 |
| `changing-positions` | 1,260 | 1,498 | 5 | 422 |
| `parking-along-roadways` | 1,674 | 2,020 | 4 | 326 |
| `freeway-driving` | 1,150 | 1,420 | 2 | 140 |
| `dealing-particular-situations` | 3,280 | 3,987 | 2 | 224 |
| `driving-night-and-bad-weather` | 2,401 | 2,935 | 2 | 150 |
| `dealing-emergencies` | 1,146 | 1,362 | 0 | 0 |
| `driving-efficiently` | 865 | 1,102 | 0 | 0 |
| `traffic-signs-and-lights` | 55 | 68 | 0 | 0 |
| `signs` | 2,280 | 2,831 | 112 | 2,136 |
| `traffic-lights` | 927 | 1,089 | 17 | 402 |
| `pedestrian-signals` | 289 | 347 | 2 | 60 |
| `pavement-markings` | 455 | 572 | 9 | 598 |
| `keeping-your-drivers-licence` | 2,061 | 2,667 | 1 | 98 |
| `other-ways-lose-your-licence` | 2,163 | 2,769 | 0 | 0 |
| `your-vehicle` | 64 | 76 | 0 | 0 |
| `maintaining-your-vehicle` | 787 | 1,003 | 2 | 204 |
| `vehicle-insurance-and-registration` | 455 | 575 | 0 | 0 |
| `towing` | 1,712 | 2,057 | 1 | 126 |
| `test-yourself-sample-knowledge-test-questions` | 370 | 526 | 0 | 0 |
| `level-two-road-test` | 5,874 | 7,058 | 11 | 414 |
| `off-road-vehicles-snowmobiles` | 8,240 | 10,391 | 17 | 682 |

</details>

<details><summary>California (DMV): per page</summary>

| Page | Words | Text tokens | Images | Image tokens |
|---|---:|---:|---:|---:|
| `index` | 276 | 349 | 2 | 98 |
| `dmv-services` | 97 | 205 | 0 | 0 |
| `copyright` | 84 | 121 | 0 | 0 |
| `disclaimer` | 43 | 65 | 0 | 0 |
| `the-california-driver-license` | 243 | 350 | 0 | 0 |
| `getting-an-instruction-permit-and-drivers-license` | 673 | 915 | 0 | 0 |
| `the-testing-process` | 839 | 1,095 | 0 | 0 |
| `changing-replacing-and-renewing-your-drivers-license` | 267 | 355 | 0 | 0 |
| `introduction-to-driving` | 858 | 1,124 | 3 | 48 |
| `navigating-the-roads` | 3,076 | 3,858 | 18 | 1,518 |
| `navigating-the-roads-cont1` | 1,731 | 2,103 | 8 | 767 |
| `laws-and-rules-of-the-road` | 1,740 | 2,256 | 26 | 1,499 |
| `laws-and-rules-of-the-road-cont1` | 2,761 | 3,526 | 11 | 1,586 |
| `laws-and-rules-of-the-road-cont2` | 1,412 | 1,782 | 0 | 0 |
| `safe-driving` | 2,176 | 2,777 | 2 | 234 |
| `safe-driving-cont1` | 744 | 897 | 1 | 144 |
| `safe-driving-cont2` | 1,235 | 1,595 | 1 | 252 |
| `alcohol-and-drugs` | 1,124 | 1,413 | 1 | 703 |
| `financial-responsibility-insurance-requirements-and-collisions` | 692 | 929 | 0 | 0 |
| `vehicle-registration-requirements` | 124 | 166 | 0 | 0 |
| `driver-safety` | 455 | 585 | 1 | 364 |
| `seniors-and-driving` | 547 | 742 | 0 | 0 |
| `glossary` | 266 | 355 | 0 | 0 |

</details>

<details><summary>Texas (DPS): per page</summary>

| Page | Words | Text tokens | Images | Image tokens |
|---|---:|---:|---:|---:|
| `index` | 1,273 | 2,006 | 3 | 2,695 |
| `chapter-1-your-license-to-drive` | 8,453 | 11,017 | 2 | 402 |
| `chapter-2-vehicle-inspection-and-registration` | 1,647 | 2,088 | 0 | 0 |
| `chapter-3-safety-responsibility` | 753 | 969 | 0 | 0 |
| `chapter-4-right-of-way` | 1,972 | 2,602 | 14 | 2,134 |
| `chapter-5-signals-signs-and-markers` | 4,213 | 5,182 | 147 | 3,728 |
| `chapter-6-signaling-passing-and-turning` | 1,346 | 1,616 | 8 | 625 |
| `chapter-7-parking-stopping-or-standing` | 1,081 | 1,287 | 7 | 1,276 |
| `chapter-8-speed-and-speed-limits` | 1,108 | 1,404 | 5 | 462 |
| `chapter-9-some-special-driving-situations` | 5,059 | 6,279 | 11 | 1,356 |
| `chapter-10-alcohol-and-drug-impact-on-the-driving-ability` | 2,954 | 4,091 | 0 | 0 |
| `chapter-11-motor-vehicle-crashes` | 1,372 | 1,737 | 0 | 0 |
| `chapter-12-pedestrian-safety` | 515 | 621 | 1 | 24 |
| `chapter-13-bicycle-laws-and-safety` | 758 | 951 | 1 | 42 |
| `chapter-14-additional-safety-tips` | 3,235 | 3,960 | 1 | 42 |
| `appendix-a-glossary-of-terms` | 3,261 | 3,909 | 0 | 0 |
| `appendix-b-driver-license-offices` | 197 | 260 | 0 | 0 |
| `appendix-c` | 1,373 | 2,077 | 0 | 0 |
| `appendix-d-fees` | 514 | 709 | 0 | 0 |
| `appendix-e-restriction-codes` | 569 | 950 | 0 | 0 |
| `back-cover` | 161 | 220 | 3 | 468 |

</details>

Regenerate with `python tools/build_corpus.py --stats` (`transformers` and the Qwen tokenizer give exact text tokens, otherwise 1.3 tokens per word).

What the numbers show:

- Each handbook fits in one long-context request: about 28k to 67k text tokens, and 7k to 13k more for the images.
- Most blocks are short (median 14 to 18 words), but 4 to 11% have more than 3 sentences, up to about 200 words. Citing such a block points to much more text than a rule usually comes from.

## Corpus: the handbooks with ids

`corpus/{mto,ca,tx}/` holds the same pages as `handbooks/`, reduced to the handbook content and given an id on every block and sentence, so that an extracted rule can point to the exact sentence it came from. Build it with `python tools/build_corpus.py`; `--check` rebuilds in memory and lists the pages whose files would change.

| | Ontario | California | Texas |
|---|---:|---:|---:|
| Pages | 30 | 23 | 21 |
| Blocks (headings, paragraphs, list items, table rows, figures) | 2,412 | 1,326 | 2,231 |
| Sentences | 3,568 | 1,681 | 3,024 |

**Ids.** Pages are numbered in table-of-contents order, starting at 1 for the cover page. Every block of a page is numbered in document order: `10.22` is block 22 of page 10 (Ontario's "Changing positions"). In a block of more than one sentence, each sentence is wrapped in `<span id="10.22.2">`; a one-sentence block is its own sentence 1. Table cells are always wrapped, so each cell can be cited. The corpus files are committed, so the ids stay fixed; rebuilding is done only on purpose.

Every image is in a `<figure>` of its own, and figures and captions are blocks with their own ids, so a rule can cite an image directly:

| Id | Block |
|---|---|
| `10.21` | A figure among the other blocks (one image), numbered like them |
| `10.21-c` | Its caption, the `<figcaption>` inside it (its sentences are `10.21-c.1`, …), whether written before or after the image |
| `6.35-f1` | An image inside a table row or a paragraph, wrapped in a figure that takes the block's id; `-f2`, `-f3` for more images in the same block |

```html
<h2 id="10.13">Passing</h2>
<figure id="10.21"><img alt="how to pass another vehicle" src="images/2-36.jpg"/><figcaption id="10.21-c">Diagram 2-46</figcaption></figure>
<p id="10.22"><span id="10.22.1">Passing within 30 metres of a pedestrian crossover is not permitted.</span> <span id="10.22.2">Passing left of a centreline is not permitted 30 metres from a bridge, viaduct or tunnel.</span> …</p>
<tr id="6.35"><td><figure id="6.35-f1"><img alt="Color: Red: …" src="images/p032-01.png"/></figure></td><td>Red: Stop, yield, or do what is posted on the sign</td></tr>
```

The ca handbook has no captions. mto has 207 and tx has 26. All 522 images have a figure: 399 among the other blocks and 123 inside table rows or a paragraph.

**What the build changes, and what it keeps.** It keeps the text exactly; the build stops if a page's text differs from `handbooks/`. It keeps headings, paragraphs, lists, tables, images, and bold and italic text. It removes the page frame (table of contents, previous and next links, "On this page", dates), links (their text stays), wrappers, and every attribute except `id`, image `src` and `alt`, list `start` and `type`, and cell spans. An image alone in a paragraph becomes a `<figure>`, and a caption paragraph right after it ("Diagram 2-46", or a Texas caption) becomes its `<figcaption>`. An image that is already in one of the handbook's own figures stays in that figure. An image inside a table cell or a paragraph with text gets a `<figure>` of its own in place. Image paths stay relative to the handbook folder; each corpus page has a `<base>` pointing there, so it shows its images in a browser.

**Manual decisions** go into `corpus/<handbook>/manual.yaml`, which the build reads. For now there is one: on Ontario's Signs page each sign is described in the paragraph before its image, and the image's alt text names no sign ("a regulatory sign"). So each image is put in one `<figure>` with that paragraph as its caption, written first as in the handbook. This was checked by looking at the images.

**Screening.** The build writes `corpus/<handbook>/screening.md`, a list of places for a person to check: figures with neither a caption nor a useful alt text, blocks of more than 3 sentences or 80 words, very short sentences (possible split errors), and paragraphs that start with a typed number. Content that is not about driving (licences, insurance, fees) is kept and not marked; it can be handled by hand later.

## Programs

The programs you run are in `tools/`. Each one starts with its usage. They can be run from any folder (Python 3.10 or later); install the dependencies once with `pip install -e '.[dev]'`.

| Program | What it does |
|---|---|
| [`tools/build_corpus.py`](tools/build_corpus.py) | Builds `corpus/` from `handbooks/`. `--check` lists the pages whose files would change, `--stats` prints the handbook analysis above |
| [`tools/build_messages.py`](tools/build_messages.py) | Writes the exact request a model gets to `build/messages/`, to read it before running anything |
| [`tools/run_extraction.py`](tools/run_extraction.py) | Runs a model on handbook pages with a prompt and saves everything in `runs/`. `--dry-run` only counts tokens |
| [`tools/extract.sh`](tools/extract.sh) | The draft gold-set extraction in one command: `tools/extract.sh [handbook] [topic]` (default `mto overtaking`; topics `overtaking`, `turning`, `parking`) runs `run_extraction.py` with Claude Opus 5.5, the `formal-rules` prompt and the whole handbook, and saves the answer to `extraction_outputs/<model>/<handbook>_<topic>_<YYYY_MM_DD>.json`. Options after the topic are passed on, e.g. `tools/extract.sh mto turning --dry-run` or `--prompt no-handbook-rules` |
| [`tools/models.py`](tools/models.py) | Lists the model presets and whether each one's key is set; `ping` checks one; `serve` starts a local vLLM server |
| [`drbench/models/models.yaml`](drbench/models/models.yaml) | The model presets |
| [`prompts/`](prompts/) | The prompts, one folder each |

**Tests:** `pytest` (no API is called).

```bash
python tools/run_extraction.py --model anthropic/claude-opus-5-5 --handbook mto --pages 10
python tools/run_extraction.py --model anthropic/claude-haiku-5-5 --handbook ca --dry-run
```

Options of `run_extraction.py`:

| Option | What it does |
|---|---|
| `--pages 9-11`, or a page file name | Which pages to send (default: the whole handbook). They go in one request, with their images and the table of contents |
| `--prompt <folder>` | Which prompt to use (default `formal-rules`) |
| `--topic <topic>` | Fills `{{topic}}` in the prompt: `overtaking`, `turning` or `parking` (see `TOPICS` in `drbench/prompts.py`) |
| `--region <id>` | Fills `{{region}}` in a closed-book prompt (`no-handbook-rules`): `ca`, `tx` or `mto`; defaults to `--handbook`. No pages are sent |
| `--set key=value` | Change a model setting for this run, e.g. `--set effort=low` or `--set extra_body.chat_template_kwargs.enable_thinking=false` |
| `--label` | Add a name to the run folder |
| `--save-to <dir>` | Also copy the answer to `<dir>/<model>/<handbook>_<topic>[_<prompt>]_<YYYY_MM_DD>.json` (`_2`, `_3` … if that file exists; `<prompt>` is left out for `formal-rules`), and the run's `meta.json` next to it as `<...>.meta.json`. A preset with a `mode` (its thinking mode) saves to `<dir>/<model>/<mode>/` |

## Prompts

A prompt is a folder in `prompts/` with three files:

| File | Where it goes |
|---|---|
| `system.md` | The system prompt: what the rules are for, what to extract, how to write and cite each rule |
| `task.md` | The request, placed at the end of the user message, after the handbook pages |
| `schema.json` | The JSON format of the answer. Claude and vLLM enforce it; other servers are only asked for it |

The prompts in `prompts/`:

| Folder | What it is |
|---|---|
| [`formal-rules/`](prompts/formal-rules/) | The current draft of the prompt for the gold set: the ground-truth rules, extracted with Claude. It is the default prompt. It writes rules in the formal grammar of the legacy Ontario passing rules: ids, force and modal, a vocabulary of defined terms, vague words with explanations, and evidence given as block ids of text, figures and captions. It covers one topic, chosen with `--topic` (overtaking, turning or parking). `no-image-rules/` (text only) and `no-handbook-rules/` (closed book, with `--region`) are variants of it. [`Note.md`](prompts/formal-rules/Note.md) explains how it is built. |
| [`smoke-test/`](prompts/smoke-test/) | A small, cheap prompt (at most three rules, cited by block id) for checking that a model and the pipeline work. Its output is not meant to be used. |
| [`archive/`](prompts/archive/) | Earlier prompts (`extract-rules`), kept for reference. Not used, and not kept up to date with the corpus or the citation format. |

The earlier rule pipeline (rule language, census, rules database, the first PDF-based Ontario rules) is on the branch [`archive/rule-pipeline`](https://github.com/hennyg888/Drive-Rule-Extraction-Bench/tree/archive/rule-pipeline).

[`prompts/Prompt_Notes.md`](prompts/Prompt_Notes.md) sums up Anthropic's advice on laying out prompts for Claude. To try a variant, copy a folder, edit it, and pass its name with `--prompt`. Every run saves a copy of the prompt it used and a hash of it, so runs with different prompt versions can be told apart.

## What a model is sent

One request per call:

- **System**: `prompts/<prompt>/system.md`.
- **User message**: the table of contents, then the pages as HTML, then `prompts/<prompt>/task.md`. The handbook comes first and the request last, the order models handle best for long documents.

The pages come from the corpus. Each page is an `<article data-page="10">` that keeps its HTML tags and block ids. The sentence `<span>`s are taken out, because they add about half as many tokens again. Every image is sent right after its `<img>` tag, so the model sees it where a reader would. This is Ontario page 10, as written by `python build_messages.py mto --pages 10` (shortened):

```html
<nav>
<h1>Contents: Official MTO Driver's Handbook (Ontario)</h1>
<ol>
<li data-page="2">Getting Your Driver’s Licence<ul><li data-ref="2.4">Requirements for driving in Ontario</li> …</ul></li>
…
</ol>
</nav>

<article data-page="10">
<h1 id="10.0">Changing positions</h1>
<p id="10.1">Changing your position on the road involves changing lanes or overtaking and passing another vehicle. Before beginning, be sure you have enough space and time to complete the move safely.</p>
<h2 id="10.2">Changing lanes</h2>
<p id="10.4">Never change lanes without giving the proper signal and looking to make sure the move can be made safely.</p>
<p id="10.5">Here are the steps for making a lane change:</p>
<ol>
<li id="10.6">Check your mirrors for a space in traffic where you can enter safely.</li>
…
<figure id="10.12"><img alt="how to make a lane change" src="images/2-35.jpg"/>
[the image 2-35.jpg itself]
<figcaption id="10.12-c">Diagram 2-45</figcaption></figure>
…
</article>

Write the formal rules that the handbook pages above state about the topic named in the last line.
…
Topic: extract formal rules about overtaking (passing another vehicle, and being passed) only.
```

Ontario page 10 alone comes to about 9,800 input tokens with its 5 images; a whole handbook fits in one request (see the analysis above).

## Grounding

After every call, `drbench/grounding.py` checks the answer's citations against the corpus and writes the result to `grounded.json`, with a count of each kind in `meta.json`. The prompts cite by block id alone (`"evidence": ["21.6", "21.7"]`), and each id is replaced with `{"block", "kind", "sentences"}`:

| Kind | Meaning |
|---|---|
| `text` | A paragraph, list item, table row or table caption; `sentences` lists its sentence ids |
| `figure` | A figure, one image (`21.7`, `6.35-f1`) |
| `caption` | A figure's caption (`21.7-c`); `sentences` lists its sentence ids |
| `heading` | A heading |
| `no-block` | The page or block does not exist |

- **no-image-rules:** ids are checked against the full corpus, so a `figure` or `caption` citation in one of these runs is an id the model was never sent.
- **no-handbook-rules:** the answer has no evidence, so there is nothing to ground.
- **Quotes:** grounding also accepts the older `{"block": "10.22", "quote": "..."}` form, used by the archived prompts. It finds the quote in the block and adds the sentence ids it covers and a `match` (`exact`, `fuzzy`, `other-block`, `heading`, `not-found` or `no-block`).

## Models

Every model is a preset in [`drbench/models/models.yaml`](drbench/models/models.yaml), and a run names one. Changing the model means changing the preset name. There are two kinds of API:

- `anthropic`: Claude through the Anthropic API, using the official SDK. Requests are streamed. Thinking is on, and `effort` sets how much. Opus and Sonnet use `fallbacks: default`: if Claude's safety classifiers decline a request, the API reruns it on a fallback model.
- `openai`: any OpenAI-compatible server. This covers the local vLLM server (`local/...` presets), the OpenAI API itself (`openai/...`) and OpenRouter (`openrouter/...`), which serves Qwen, Gemini, GPT and Claude under one key.

Adding a model on one of these APIs takes only a new preset: copy one and change `model` (and `base_url` for another server). Another kind of API needs a new class in `drbench/models/`, next to `claude.py`.

**Keys** go in `.env` at the repository root, one `NAME=value` per line. Git ignores the file. `ANTHROPIC_API_KEY` is needed for Claude, `OPENAI_API_KEY` for the OpenAI API, `OPENROUTER_API_KEY` for OpenRouter; local presets need no key. Instead of an Anthropic key, `ant auth login` also works.

**Local models.** Start the server with `python tools/models.py serve local/qwen3.8-27b`, wait until it reports `Application startup complete`, then run with that preset. The `serve` line of each local preset shows how many GPUs it uses. Stop the server (Ctrl-C) when you are done, because the GPUs are shared. The presets of the benchmark's local models decode greedily and empty vLLM's image cache before every request, so that a fixed prompt gives the same answer; the comments in `models.yaml` explain each setting, and [`extraction_outputs/README.md`](extraction_outputs/README.md) records the runs made with them.

## Runs

A run writes `runs/<time>-<preset>-<handbook>/`:

| File | What it holds |
|---|---|
| `meta.json` | The run settings (preset, model settings, handbook, pages, prompt name and hash, git commit) and the results: tokens, seconds, estimated cost, stop reason, and citation matches |
| `prompt/` | A copy of the prompt folder used |
| `request.md` | The user message as text, with `[image: src]` where each image was |
| `response.json`, `output.txt`, `reasoning.txt` | The whole API response, the answer, and the model's reasoning when the API returns it |
| `output.json`, `grounded.json` | The answer as JSON, and the same with every cited block id expanded to its kind and sentence ids (see [Grounding](#grounding)) |

Runs are not committed (`runs/` is in `.gitignore`). To keep a run, copy it somewhere tracked, or add it with `git add -f`.

Answers saved with `--save-to extraction_outputs` are committed, with their `.meta.json`, in [`extraction_outputs/`](extraction_outputs/), by vendor, model and thinking mode. Its [README](extraction_outputs/README.md) records the candidate model runs on Ontario overtaking.

## The handbook copies (`handbooks/`)

`handbooks/<id>/` (`mto`, `ca`, `tx`) holds each handbook as downloaded, before any corpus processing: one HTML page per handbook page, its `images/`, a `style.css`, and `index.html` to browse it in a browser. `source/` holds the published PDF. The scripts in `scrapers/` made these folders, and `tools/build_corpus.py` builds `corpus/` from them.

The HTML text and images are unedited. The scrapers only removed the site's header, footer, menus and scripts, pointed links and images at the local files, and added navigation. Ontario and California were checked word for word against the live sites (October 2026). Texas publishes only a PDF, so its pages are converted from `source/DL-7.pdf` (`scrapers/scrape_tx_handbook.py --verify` checks the conversion).
