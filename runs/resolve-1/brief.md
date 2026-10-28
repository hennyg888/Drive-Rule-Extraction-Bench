# Resolving flagged words: brief for one batch

R = the working folder: `ground/` is this repository, and `resolve/` held the inputs (handbook.txt, every sentence and figure of the Ontario handbook from the database; provisions.txt, the provisions then in the database; and the flag batches). The answers, checked against the handbook and the local copies of the law, are `resolved.json`, loaded by `tools/resolve_flags.py`.

Rules for this task:
- Do NOT call any mcp__hearthbot__ tools. Do not install packages. Do not use web search or fetch.
- Read only the files named here. Write only the one output file named in your task. Do not touch the database or any repo file.
- Use python3 -I -B if you run Python; grep, sed and similar are fine.

## The job

Ontario driver's-handbook rules were extracted into a rule language, and vague or unclear words in them were flagged. Each flag has a code:

| Code | Meaning |
|---|---|
| J | Judgment term: safe, enough, sure, carefully, too closely, ... |
| S | Hedged scope: usually, often, many, some, ... |
| R | Unclear reference or role ("these lanes", "where required") |
| M | Unclear legal strength: is it a legal duty or advice? |
| D | Implicit default: a permission that presupposes an unstated prohibition, or the reverse |
| V | Wording drift: the handbook uses different words for the same thing |
| X | The same rule is stated again elsewhere in the handbook, possibly differently |

Your job is to resolve the ambiguity of every flag in your batch, as far as the sources allow, by searching two places:

1. **The handbook, anywhere in it**: other sentences of the same paragraph, other pages, the Level One and Level Two road test pages, the G1 knowledge sections, figure captions, the offence tables. The handbook is in R/resolve/handbook.txt, one line per sentence or figure: unit id, locator (page › heading path · paragraph), text. Grep it widely (stems, synonyms, numbers, units like "metres" and "seconds"). The flagged sentence itself does not count as an answer, but its neighbours do.
2. **The law**: the Highway Traffic Act and four regulations, plain text, in R/ground/statutes/on/hta/hta.txt, reg-339-94/940339.txt (demerit points), reg-455-07/070455.txt (stunts), reg-608/900608.txt (trucks in left lanes), reg-615/900615.txt (signs). Provisions already in the database are in R/resolve/provisions.txt (id, citation, heading, text); cite those by id.

Your batch of flags is a JSON file (named in your task). Each entry has: the flag id, run, code, span (the flagged words), the flag's note, the statement it belongs to, the statement's source sentences, and `now`/`now_links`: what an earlier pass recorded. That earlier pass often searched only the law, and kept one status per flag, so a handbook answer could be hidden behind a law status. Use it as a lead, check it, and keep what is right.

## What to record for each flag

For each side (handbook, law), one finding:

| Finding | Meaning |
|---|---|
| DEFINES | Gives a definition, number, measure or test that makes the flagged words checkable (for every case or only some; say which in `says`) |
| STATES | Settles the flag without a measure: makes it a legal duty or not (M), names the referent (R), says the default outright (D), shows the variant words name the same thing (V), or states the same rule in agreeing words (X) |
| REPEATS | Uses the same open words, or equally open ones, so it does not settle the flag |
| SILENT | Says nothing on it |

Then one verdict for the flag:

| Verdict | Meaning |
|---|---|
| RESOLVED | Some source settles it for every case the statement covers |
| PARTIAL | Settled only for some cases (e.g. a measure for a lane change but none for a pass on a two-lane road), or narrowed but not settled |
| OPEN | Nothing settles it |

Guidance by code:
- J: a measure is DEFINES (the road test's "two- to three-second gap", "150 metres", "one metre"). The law asking the driver to "first ascertain that it can be done safely" is REPEATS, not a measure. Never invent a threshold, and never count a number that is about something else.
- S: DEFINES when a source lists exactly which (e.g. a regulation's schedule of highways); otherwise REPEATS or SILENT.
- M: law STATES when a provision makes it a duty (or the handbook's offence table / "It's the law" sentence does: that is handbook STATES). If the law covers only part of the statement, PARTIAL.
- V: DEFINES when a source defines the word; STATES when a source shows the variants mean the same thing; say which word the law uses.
- X: cite the other sentence(s) that state it. If they agree, handbook STATES and RESOLVED; if they differ, say how in `says` and give PARTIAL or OPEN unless the law settles which reading is right.

## Output

Write a JSON array to the output file named in your task, one object per flag of your batch, in batch order, every flag included:

```
{"id": "<flag id, exactly as given>",
 "handbook": {"finding": "DEFINES|STATES|REPEATS|SILENT", "says": "<one sentence: what the handbook says about these words, with the key words quoted>", "units": ["<handbook unit ids from handbook.txt>"]},
 "law": {"finding": "DEFINES|STATES|REPEATS|SILENT", "says": "<one sentence: what the law says, citing sections>", "units": ["<provision ids>"]},
 "verdict": "RESOLVED|PARTIAL|OPEN",
 "definition": "<the reading that resolves it, for the cases it covers; null when OPEN>",
 "effect": "<what it would change in the statement, or null>",
 "note": "<optional: anything a reviewer should know, or null>"}
```

- `units` are required for DEFINES, STATES and REPEATS, and empty for SILENT. Every handbook unit id must be a line of handbook.txt whose text supports `says`; quote its key words in `says`.
- A law provision not in provisions.txt: give it as `{"id": "on-hta:<section>", "file": "<path>", "text": "<the provision copied word for word from the file>"}` inside `units` instead of a bare id, using the id style of provisions.txt (on-hta:142(1), on-hta:154(1)(a), on-reg-339-94:item-13). Prefer the smallest subsection that says it.
- `says` describes only its own side. Write in plain English, no Rule Language keywords.
- Two flags with the same words in different statements can share findings, but write each one out in full.

Final reply: only the counts by verdict, by handbook finding and by law finding, and the number of new provisions, in under 60 words.
