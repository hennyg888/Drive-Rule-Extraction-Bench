# Selecting a topic's passages from a whole handbook

Extraction (`extract-rules.md`) works on passages already chosen for a topic. This file says how to choose them, so that every handbook's topic set is built the same way as michael's Ontario passing set (`analysis/passing-rules/mto/inputs/passing-passages.json`, 96 passages, plus 9 the census added).

## Input

The handbook split into passages by `tools/segment_handbook.py`: one per paragraph, list item, table row or figure, each with its page, heading path and text.

## What to select

1. **The topic's home section** (for passing, the section or chapter that defines passing and gives its procedure): every passage in it, including introductions, figures and summaries. Mark them `intro` (definitions, scope, why), `general` (principles and the normal procedure) or `specific` (special situations).
2. **Everything in scope elsewhere in the handbook** (Part C of `extract-rules.md` defines scope): read every page, not only pages whose titles sound relevant. Passing content hides in sections on sharing the road (cyclists, motorcycles, trucks, farm vehicles, horses), stopping (school buses, crosswalks), pavement markings, signs (regulatory signs, no-passing pennants), weather and night driving, freeways, towing, emergency vehicles, offences and penalties, and sample test questions. Mark them `specific`.
3. **Context passages a selected passage depends on**: a section introduction that makes its rules law ("These signs give a direction that must be obeyed"), a list lead sentence, a neighbour that a pronoun refers to, a penalty stated in another paragraph, and the figure that shows a rule. Select them, with the part of the passage they support.
4. **Near misses, as negatives.** Some passages look in scope but should give no statement on the topic: "pass" meaning something else ("wait for the train to pass", "pass carefully" around an animal or a work zone), or a lane-change or turn item filed under a passing heading. They are useful test items, because a good extraction writes nothing for them. Select a few and mark them `excluded`.

Keep whole passages; don't cut sentences out. A long paragraph with one in-scope sentence is selected whole; extraction quotes only that sentence.

## What not to select

Licensing, insurance and registration text, unless it states a penalty for a passing offence; passages that only mention a passing lane or "passing" in passing (a list of driving skills, a test checklist), unless they state a rule.

## Output

A JSON list, one entry per selected passage, in handbook order: `{"seg": "<segment id>", "part": "intro|general|specific|excluded", "why": "<one line>"}`. `tools/make_passages.py` turns it into the passage file that extraction reads.
