# The rules database

One SQLite database holds the handbooks sentence by sentence, the statements extracted from them, the
rule language vocabulary, the laws behind the statements, and the grounding of every flagged word. It
replaces reading documents by eye with fixed queries: the same question always gets the same answer.

- `db/tables/<table>.jsonl` is the master copy, in git: one row per line, sorted by key.
- `db/rules.sqlite` is built from it and is not in git.
- `db/schema.sql` defines the tables, with a comment on each.
- `tools/db.py` loads, checks, dumps and exports.
- `tools/db_import.py` made the first version from the files it replaced (27 October 2026). Do not run
  it again: it would drop everything added since. The census tables it made were removed on 28
  October; tagging (stage 2 below) replaces them.

## The stages

Every stage after the first reads the database and writes the database; none reads the handbook's
HTML again. Each stage has one job, and each pass of a stage is a `run` row saying what it read,
with which prompt (and its sha256) and by whom.

| Stage | Job | Tool | Writes |
|---|---|---|---|
| 1 Import | Put the handbook in, one row per paragraph and per sentence, word for word | `tools/import_handbook.py mto --sentences` | `page`, `unit` |
| 2 Tag | Label every sentence and figure from fixed lists (type, modal as written, caution, topics, vague words), by an LLM with `prompts/tag-units.md`; never rewrite | `tools/tag_units.py shard`, the model, `check`, `load` | `run`, `unit_tag`, `unit_topic`, `unit_vague` |
| 3 Select | Choose a topic's paragraphs by a fixed query on the tags; a person confirms, adding or dropping by hand | `tools/select_passages.py` | `run`, `selection` |
| 4 Formalize | Write the selected paragraphs as rule-language statements with `prompts/extract-rules.md`: each paragraph goes in whole, its sentences numbered (`p44.1`), and each statement cites the sentences (or figures) it comes from | `tools/extract_rules.py render`, the model, `check`, `load`; on-passing-1, answered before sentences were numbered, got its sentences from `runs/on-passing-1/cite_sentences.py` | `run`, `statement` and its child tables, `term`, `occurrence` |
| 5 Ground | Resolve every flag by searching the rest of the handbook and the law, recording what each side says and a verdict; then put the law under the statements: the provisions behind each statement, law lines | Flags: a model with `runs/resolve-1/brief.md`, loaded by `tools/resolve_flags.py`. Law under the statements: `tools/carry_grounding.py` carries what was checked for a paired statement of another run, the rest by hand (for on-passing-1, `runs/on-passing-1/ground_paired.py` and `ground_unpaired.py`, which also made the first, law-only pass at the flags that `resolve-1` replaced). All checked by `db.py check` | `grounding`, `grounding_finding`, `grounding_link`, `statement_basis`, `statement_law`, `statement_law_ref` |
| 6 Validate | Fixed checks on everything above, and comparison of two runs | `tools/db.py check`, `tools/compare_runs.py` | nothing |

```
python3 tools/import_handbook.py mto --sentences
python3 tools/tag_units.py shard mto on-tag-1 --shards 8        # then a model answers each shard
python3 tools/tag_units.py check on-tag-1
python3 tools/tag_units.py load on-tag-1 --model NAME --date YYYY-MM-DD
python3 tools/select_passages.py mto passing on-passing-select-1 --tags on-tag-1 [--add ID --drop ID --by NAME]
python3 tools/extract_rules.py render on-passing-1 --selection on-passing-select-1   # then a model answers
python3 tools/extract_rules.py check on-passing-1
python3 tools/extract_rules.py load on-passing-1 --model NAME --date YYYY-MM-DD
python3 tools/compare_runs.py on-passing-1 on-passing-ref --report runs/on-passing-1/compare.md
python3 tools/carry_grounding.py on-passing-1 --from on-passing-ref --report runs/on-passing-1/grounding-left.md
python3 tools/resolve_flags.py runs/resolve-1/resolved.json      # a model's answers to runs/resolve-1/brief.md
python3 tools/db.py check && python3 tools/db.py dump
```

A model's inputs and answers stay in `runs/<run>/`: the rendered prompt, the inputs, the answers and
the brief it was given.

## Working with it

```
python3 tools/db.py load            # db/tables -> db/rules.sqlite
sqlite3 db/rules.sqlite             # query and change it (or Python's sqlite3)
python3 tools/db.py check           # every check below; exit 1 on an error
python3 tools/db.py dump            # db/rules.sqlite -> db/tables, then commit
python3 tools/db.py export --write  # rewrite rules.json and passing-rules-law.md from it
```

After changing statements, run `export --write` and then `tools/render_rules_md.py` so `rules.json`
and `passing-rules.md` follow. `export --write` also writes `passing-rules-law.md` for a jurisdiction
with law lines. `check` fails while either file differs from the database.

Load, then dump, gives the same files byte for byte, and export gives the same `rules.json` byte for
byte, so a change shows in git as exactly the rows it touched.

## Tables

| Table | One row per |
|---|---|
| `source` | Document: a handbook, a statute, a regulation, a standard or a safety model, with its version, URL, local copy and sha256 |
| `page` | Handbook page, in reading order, with its title |
| `unit` | Citable piece of a document, word for word: a handbook paragraph (or figure, with its caption), a sentence of a paragraph, a topic passage of a reviewed set, or a provision of a law |
| `run` | Pass of a stage: tagging, selection or extraction, with what it read, its prompt and sha256, who did it and when; `rules_json = 1` marks the set `rules.json` holds |
| `unit_tag`, `unit_topic`, `unit_vague` | Tags of a sentence or figure: type, modal as written, caution; the topics it is about; its vague words, copied exactly, with a flag code |
| `selection` | Paragraph a selection run chose for a topic, with the passage id the extraction prompt shows (`p17`) and why: tag, lead of a list, or by hand |
| `vocabulary` | Fixed word of the rule language: types, modals (with their strength), clauses, connectives, links, flags, verbs, roles, units |
| `statement` | Extracted statement, with the run it came from; the reviewed set is the one in `rules.json` |
| `statement_step`, `statement_source`, `step_source`, `statement_figure` | A procedure's steps, and the passages (reviewed set) or the sentences and figures (pipeline runs) a statement or step cites |
| `statement_link` | EXCEPTION TO, SPECIALIZES or a plain reference between statements |
| `statement_basis` | Provision behind a statement, and whether the statement says the SAME, is BROADER or NARROWER, DIFFERENT, or the provision is its PENALTY |
| `occurrence` | Flag on a statement (rule language §8) |
| `term` | Flagged judgment word, per jurisdiction (`on:safely`), so every use of one word can be found |
| `grounding` | A flag's verdict (RESOLVED, PARTIAL, OPEN), the reading that resolves it, and its effect on the statement |
| `grounding_finding` | What the rest of the handbook and what the law (and, rarely, an engineering standard) say about a flag |
| `grounding_link` | The handbook sentences and the provisions each finding rests on |
| `statement_law`, `statement_law_ref` | Law added under a statement, which itself stays as extracted: a line in the rule language saying what the law says on the statement's subject (the same duty, the duty the handbook words as advice, the law's definitions, conditions, exceptions or penalty), and the provisions it cites |

Two tables are rebuilt by `load` and `check`, never dumped: `passage_part` (which sentences or
paragraphs a topic passage covers, matched by text, or by image for a figure) and `statement_part`
(each statement split at its keywords).

`analysis/passing-rules/mto/passing-rules-law.md` shows every Ontario statement as extracted, with
its flags and their notes unchanged, and under it what the handbook and the law say about each flag
and the verdict, the law lines, and each provision behind the statement with how the statement compares with
it. Each provision is quoted word for word at the end, with a link to its line in `statutes/` and to
e-Laws.

Ids say what they point at: `mto:para:driving-along:018` (a paragraph), `mto:sent:stopping:022.1`
(the first sentence of paragraph `mto:para:stopping:022`), `mto:passage:m17` (a
passage of the reviewed set), `on-hta:148(8)` (a provision), `on-reg-339-94:item-12` (a row of the
demerit point table), `mto:3.1.2a` (a reviewed statement), `on-passing-1:p17a` (a statement of
extraction run `on-passing-1`), `mto:3.1.2a|R|30 m from` (a flag).

### Resolving flags

Each flag gets one finding per side, the handbook (anywhere but the flagged sentence itself) and the
law:

| Finding | Meaning |
|---|---|
| `DEFINES` | Gives a definition, number, measure or test that makes the flagged words checkable (for every case or only some) |
| `STATES` | Settles the flag without a measure: makes it a legal duty or not, names the referent, says the default outright, shows variant words name the same thing, or states the same rule in agreeing words |
| `REPEATS` | Uses the same open words, or equally open ones |
| `SILENT` | Says nothing on it |

and one verdict: `RESOLVED` (settled for every case the statement covers), `PARTIAL` (settled for some
cases, or narrowed), `OPEN` (nothing settles it).

## Checks

Errors (exit 1):
- a row refers to a row that does not exist;
- a law's local copy does not match its sha256, or a provision is not word for word in its local copy
  (spacing and curly quotes aside);
- a statement cites nothing; a statement or step of a run with no selection (the reviewed set, the
  California and Texas drafts) cites something that is not a topic passage; one of a pipeline run cites
  something that is not a sentence or figure of its run's selection (a whole text paragraph is not enough);
- a run reads the wrong kind of run (selection reads tags, extraction reads a selection, same
  handbook), or statements belong to a run that is not an extraction;
- a tag is on something other than a sentence or figure, a figure is not tagged FIGURE (or text is),
  a vague word is not copied exactly from its sentence, or a selected unit is not a paragraph of the
  run's handbook;
- a statement's strength does not match its modal, or a DEFINE or FACT has a strength;
- an EXCEPTION TO or SPECIALIZES link is not in the statement's text;
- a basis row points at something that is not a provision; a grounding link points at the wrong kind
  of source for its role; a flag's grounding lacks a handbook or a law finding; a `SILENT` side has
  links, or another side none; a verdict other than `OPEN` has no `DEFINES` or `STATES` finding or no
  definition;
- a law line has an advice modal or no modal; cites a provision that is not a basis row of its
  statement; cites no statute or regulation provision other than a penalty; states a penalty
  (`IF VIOLATED`) without citing a PENALTY provision; or marks open (`[?…]`) a word the law settles
  (law finding `DEFINES` or `STATES`);
- `rules.json` or `passing-rules-law.md` differs from the database.

Warnings: a quote not word for word in its passage, a passage that matches no handbook text, a
capitalised word not in the vocabulary (in a statement or a law line), a J, S, R, G, M or D flag whose
span is not in the statement, its steps or its sources, a law with no local copy.

Reported each time: flags by verdict, what the handbook and the law say about them, LAW statements that cite no provision, ADVICE
statements with a provision behind them, law lines and the statements with a provision behind them
that have none yet, topic passages no statement cites, how many sentences and figures each tagging
run tagged, and for each extraction run how many handbook sentences it cites.

## Questions it answers

Sentences and figures tagged with an extraction run's topic that none of its statements cites:

```sql
SELECT id, locator, text FROM topic_unit_unused WHERE run_id = 'on-passing-1';
```

The tags of one paragraph's sentences, and every vague word tagged on a page:

```sql
SELECT u.id, t.type, t.modal, t.caution, u.text FROM unit u JOIN unit_tag t ON t.unit_id = u.id
WHERE u.parent_id = 'mto:para:changing-positions:012' ORDER BY u.id;
SELECT v.code, v.span, u.text FROM unit_vague v JOIN unit u ON u.id = v.unit_id WHERE u.page = 'changing-positions';
```

Which statements cite a handbook sentence:

```sql
SELECT statement_id FROM unit_use WHERE unit_id = 'mto:sent:stopping:022.1';
```

What depends on what:

```sql
SELECT from_id, kind, to_id FROM statement_link ORDER BY from_id;
```

Every flag still open, and every use of one word:

```sql
SELECT * FROM ungrounded_flag WHERE jurisdiction = 'ca';
SELECT o.statement_id, g.verdict, g.definition FROM occurrence o LEFT JOIN grounding g ON g.occurrence_id = o.id
WHERE o.term_id = 'on:safely';
```

What the handbook and the law say about each flag of a run, and what each rests on:

```sql
SELECT o.id, g.verdict, f.side, f.finding, f.says, group_concat(l.unit_id, ', ')
FROM occurrence o JOIN statement s ON s.id = o.statement_id
JOIN grounding g ON g.occurrence_id = o.id JOIN grounding_finding f ON f.occurrence_id = o.id
LEFT JOIN grounding_link l ON l.occurrence_id = o.id AND (l.role = f.side OR f.side = 'standard' AND l.role = 'model')
WHERE s.run_id = 'on-passing-1' GROUP BY o.id, f.side;
```

Statements the handbook words as advice but a law states, and LAW statements with no provision yet:

```sql
SELECT statement_id, unit_id, relation, note FROM advice_with_law;
SELECT * FROM law_without_basis;
```

Each Ontario statement with the law lines added under it and the provisions they cite, and the
statements with a provision behind them that have no law line yet:

```sql
SELECT s.local_id, s.text, l.text, group_concat(r.unit_id, ', ')
FROM statement s JOIN statement_law l ON l.statement_id = s.id
JOIN statement_law_ref r ON r.statement_id = l.statement_id AND r.position = l.position
GROUP BY l.statement_id, l.position ORDER BY s.position, l.position;
SELECT * FROM law_not_added;
```

## Changing it

```sql
-- record a flag no source settles
INSERT INTO grounding (occurrence_id, verdict, note) VALUES ('ca:p103c|J|safely', 'OPEN', 'No source.');
INSERT INTO grounding_finding VALUES ('ca:p103c|J|safely', 'handbook', 'SILENT', NULL),
                                     ('ca:p103c|J|safely', 'law', 'SILENT', NULL);

-- correct one
UPDATE grounding SET note = 'No source found in the Vehicle Code.' WHERE occurrence_id = 'ca:p103c|J|safely';

-- remove one, links and findings first
DELETE FROM grounding_link WHERE occurrence_id = 'ca:p103c|J|safely';
DELETE FROM grounding_finding WHERE occurrence_id = 'ca:p103c|J|safely';
DELETE FROM grounding WHERE occurrence_id = 'ca:p103c|J|safely';
```

Then `check`, `dump`, and commit the changed `db/tables/*.jsonl`. A new law goes in as a `source` row
with its local copy under `statutes/` and its sha256, then one `unit` row per provision, copied word
for word; `check` confirms each against the copy.
