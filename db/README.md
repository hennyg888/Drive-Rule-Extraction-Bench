# The rules database

One SQLite database holds the handbooks sentence by sentence, the statements extracted from them, the
rule language vocabulary, the laws behind the statements, and the grounding of every flagged word. It
replaces reading documents by eye with fixed queries: the same question always gets the same answer.

- `db/tables/<table>.jsonl` is the master copy, in git: one row per line, sorted by key.
- `db/rules.sqlite` is built from it and is not in git.
- `db/schema.sql` defines the tables, with a comment on each.
- `tools/db.py` loads, checks, dumps and exports.
- `tools/db_import.py` made the first version from the files it replaced (27 October 2026). Do not run
  it again: it would drop everything added since.

## Working with it

```
python3 tools/db.py load            # db/tables -> db/rules.sqlite
sqlite3 db/rules.sqlite             # query and change it (or Python's sqlite3)
python3 tools/db.py check           # every check below; exit 1 on an error
python3 tools/db.py dump            # db/rules.sqlite -> db/tables, then commit
python3 tools/db.py export --write  # rewrite analysis/passing-rules/*/rules.json from it
```

After changing statements, run `export --write` and then `tools/render_rules_md.py` so `rules.json`
and `passing-rules.md` follow. `check` fails while `rules.json` differs from the database.

Load, then dump, gives the same files byte for byte, and export gives the same `rules.json` byte for
byte, so a change shows in git as exactly the rows it touched.

## Tables

| Table | One row per |
|---|---|
| `source` | Document: a handbook, a statute, a regulation, a standard or a safety model, with its version, URL, local copy and sha256 |
| `unit` | Citable piece of a document, word for word: a handbook paragraph, an Ontario sentence, a topic passage, or a provision of a law |
| `sentence_label` | Ontario sentence's census label: type, role, modal, where its strength comes from, whether it is about passing |
| `sentence_word` | Word the census pulled out of a sentence: its action, entities, situation dimensions, vague words (with their flag code), clause keywords |
| `vocabulary` | Fixed word of the rule language: types, modals (with their strength), clauses, connectives, links, flags, verbs, roles, units |
| `statement` | Extracted statement, as in `rules.json` |
| `statement_step`, `statement_source`, `step_source`, `statement_figure` | A procedure's steps, and the passages and figures a statement or step cites |
| `statement_link` | EXCEPTION TO, SPECIALIZES or a plain reference between statements |
| `statement_basis` | Provision behind a statement, and whether the statement says the SAME, is BROADER or NARROWER, DIFFERENT, or the provision is its PENALTY |
| `occurrence` | Flag on a statement (rule language §8) |
| `term` | Flagged judgment word, per jurisdiction (`on:safely`), so every use of one word can be found |
| `grounding`, `grounding_link` | How far a formal source settles a flag, and the provisions or sentences that do |

Two tables are rebuilt by `load` and `check`, never dumped: `passage_part` (which sentences or
paragraphs a topic passage covers, matched by text, or by image for a figure) and `statement_part`
(each statement split at its keywords).

Ids say what they point at: `mto:para:driving-along:018` (a paragraph), `mto:sent:stopping:022.1`
(a census sentence), `mto:passage:m17` (a topic passage), `on-hta:148(8)` (a provision),
`on-reg-339-94:item-12` (a row of the demerit point table), `mto:3.1.2a` (a statement),
`mto:3.1.2a|R|30 m from` (a flag).

### Grounding statuses

| Status | Meaning |
|---|---|
| `LAW_DEFINES` | The law gives the definition or the number |
| `LAW_STATES` | The law states the duty itself, which settles the flag's strength, scope or reference |
| `LAW_REPEATS` | The law uses the same open word, so the vagueness is in the law too |
| `STANDARD` | The law leaves it open and an engineering standard or safety model gives an operational definition (a proxy, not law) |
| `HANDBOOK` | Another part of the handbook settles it |
| `OPEN` | No formal source settles it |

## Checks

Errors (exit 1):
- a row refers to a row that does not exist;
- a law's local copy does not match its sha256, or a provision is not word for word in its local copy
  (spacing and curly quotes aside);
- a statement cites something that is not a topic passage;
- a statement's strength does not match its modal, or a DEFINE or FACT has a strength;
- an EXCEPTION TO or SPECIALIZES link is not in the statement's text;
- a basis row points at something that is not a provision; a grounding link points at the wrong kind
  of source for its role; a `LAW_*` grounding has no law provision, or a `STANDARD` one no standard;
- `rules.json` differs from the database.

Warnings: a quote not word for word in its passage, a passage that matches no handbook text, a
capitalised word not in the vocabulary, a J, S, R or G flag whose span is not in the statement, its
steps or its sources, a law with no local copy.

Reported each time: flags by grounding status, LAW statements that cite no provision, ADVICE
statements with a provision behind them, topic passages no statement cites, and how many handbook
sentences are cited.

## Questions it answers

Ontario sentences the census marked as about passing that no statement cites:

```sql
SELECT id, locator, text FROM passing_sentence_unused;
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
SELECT o.statement_id, g.status FROM occurrence o LEFT JOIN grounding g ON g.occurrence_id = o.id
WHERE o.term_id = 'on:safely';
```

The provisions that settle each Ontario flag:

```sql
SELECT o.id, g.status, u.locator, u.text
FROM occurrence o JOIN grounding g ON g.occurrence_id = o.id
JOIN grounding_link l ON l.occurrence_id = o.id JOIN unit u ON u.id = l.unit_id
WHERE o.statement_id LIKE 'mto:%' AND l.role = 'law';
```

Statements the handbook words as advice but a law states, and LAW statements with no provision yet:

```sql
SELECT statement_id, unit_id, relation, note FROM advice_with_law;
SELECT * FROM law_without_basis;
```

## Changing it

```sql
-- settle a flag
INSERT INTO grounding (occurrence_id, status, note)
VALUES ('ca:p103c|J|safely', 'OPEN', 'No source.');

-- correct one
UPDATE grounding SET note = 'No source found in the Vehicle Code.' WHERE occurrence_id = 'ca:p103c|J|safely';

-- remove one, links first
DELETE FROM grounding_link WHERE occurrence_id = 'ca:p103c|J|safely';
DELETE FROM grounding WHERE occurrence_id = 'ca:p103c|J|safely';
```

Then `check`, `dump`, and commit the changed `db/tables/*.jsonl`. A new law goes in as a `source` row
with its local copy under `statutes/` and its sha256, then one `unit` row per provision, copied word
for word; `check` confirms each against the copy.
