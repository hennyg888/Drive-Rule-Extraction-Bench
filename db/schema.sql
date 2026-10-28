-- The rules database. db/tables/<table>.jsonl in git is its text form; tools/db.py loads it into
-- db/rules.sqlite, checks it, and dumps it back. See db/README.md.

-- Documents ----------------------------------------------------------------------------------

CREATE TABLE source (
  id           TEXT PRIMARY KEY,            -- 'mto-handbook', 'on-hta'
  kind         TEXT NOT NULL CHECK (kind IN ('handbook', 'statute', 'regulation', 'standard', 'model')),
  jurisdiction TEXT NOT NULL,               -- 'on', 'ca', 'tx', or 'any' for a safety model
  title        TEXT NOT NULL,
  citation     TEXT,                        -- 'R.S.O. 1990, c. H.8'
  version      TEXT,                        -- the edition or consolidation the document states
  url          TEXT,
  path         TEXT,                        -- the local copy in this repo
  sha256       TEXT,
  retrieved    TEXT
);

-- A handbook's pages in reading order (tools/import_handbook.py).
CREATE TABLE page (
  source_id TEXT NOT NULL REFERENCES source(id),
  id        TEXT NOT NULL,                  -- the page file, without .html
  position  INTEGER NOT NULL,
  title     TEXT NOT NULL,
  PRIMARY KEY (source_id, id),
  UNIQUE (source_id, position)
);

-- Every citable piece of a document, verbatim.
--   paragraph  a handbook paragraph, list item, step or figure (analysis/segments/)
--   sentence   one sentence of a text paragraph, split by tools/import_handbook.py (Ontario only)
--   passage    a passage chosen by hand for a topic (inputs/); it covers sentences or paragraphs
--   provision  a subsection or clause of a law or regulation, or a part of a standard
CREATE TABLE unit (
  id        TEXT PRIMARY KEY,               -- 'mto:para:driving-along:018', 'mto:sent:index:001.1', 'mto:passage:m17', 'on-hta:148(8)'
  source_id TEXT NOT NULL REFERENCES source(id),
  kind      TEXT NOT NULL CHECK (kind IN ('paragraph', 'sentence', 'passage', 'provision')),
  parent_id TEXT REFERENCES unit(id),       -- a sentence's paragraph
  page      TEXT,                           -- handbook page file, without .html
  locator   TEXT NOT NULL,                  -- 'Driving along › Maintaining space · ¶2', 's. 148 (8)'
  heading   TEXT,                           -- a provision's marginal heading, or a figure's caption
  anchor    TEXT,                           -- the h2 id on the page, for links
  image     TEXT,                           -- a figure's image path
  valid_from TEXT,                          -- a provision in force from this date, when it is not yet
  valid_to   TEXT,                          -- a provision replaced on this date
  text      TEXT NOT NULL
);

-- Which sentences or paragraphs a topic passage covers (matched by text, or by image for figures).
CREATE TABLE passage_part (
  passage_id TEXT NOT NULL REFERENCES unit(id),
  part_id    TEXT NOT NULL REFERENCES unit(id),
  PRIMARY KEY (passage_id, part_id)
);

-- Runs -----------------------------------------------------------------------------------------

-- One pass of a pipeline stage over one handbook (pipeline/PIPELINE.md): tagging its sentences and
-- figures, selecting a topic's passages from the tags, or extracting a topic's statements from a
-- selection. Each stage reads only what an earlier run wrote to the database.
CREATE TABLE run (
  id            TEXT PRIMARY KEY,           -- 'on-tag-1', 'on-passing-select-1', 'on-passing-1'
  stage         TEXT NOT NULL CHECK (stage IN ('tag', 'select', 'extract')),
  source_id     TEXT NOT NULL REFERENCES source(id),   -- the handbook
  topic         TEXT,                       -- select and extract: 'passing'
  input_run     TEXT REFERENCES run(id),    -- the run whose rows it read
  rules_json    INTEGER NOT NULL DEFAULT 0, -- 1: its statements are the topic's rules.json
  prompt        TEXT,                       -- the prompt file, from the repo root
  prompt_sha256 TEXT,
  model         TEXT,                       -- who did it: a model, or a person for a reviewed set
  date          TEXT,
  note          TEXT
);

-- Stage 2, tagging. Labels an LLM gave each handbook sentence and figure with prompts/tag-units.md,
-- each picked from a fixed list. They describe the text and never rewrite it; writing rules is
-- stage 4.
--   type     RULE (an instruction, permission or piece of advice), STEP (one step of a sequence),
--            DEFINE, FACT, CONSEQ (a penalty or other consequence), META (navigation, a reference,
--            a question), FIGURE (a figure)
--   modal    the force the wording itself gives, before any reading of the law: MUST, MUST NOT, MAY,
--            SHOULD, SHOULD NOT, IMPERATIVE ("Keep right"), IMPERATIVE NOT ("Do not pass", "Never"),
--            NONE
--   caution  1 when it tells the driver to watch out for something
CREATE TABLE unit_tag (
  unit_id TEXT PRIMARY KEY REFERENCES unit(id),
  run_id  TEXT NOT NULL REFERENCES run(id),
  type    TEXT NOT NULL CHECK (type IN ('RULE', 'STEP', 'DEFINE', 'FACT', 'CONSEQ', 'META', 'FIGURE')),
  modal   TEXT NOT NULL CHECK (modal IN ('MUST', 'MUST NOT', 'MAY', 'SHOULD', 'SHOULD NOT', 'IMPERATIVE',
                                         'IMPERATIVE NOT', 'NONE')),
  caution INTEGER NOT NULL CHECK (caution IN (0, 1))
);

-- The topics a sentence or figure is about, from the tagging prompt's list ('passing').
CREATE TABLE unit_topic (
  unit_id TEXT NOT NULL REFERENCES unit_tag(unit_id),
  topic   TEXT NOT NULL,
  PRIMARY KEY (unit_id, topic)
);

-- Vague wording the tagging found in a sentence: its words, verbatim, and a flag code of rule
-- language §8 (J judgment, M unclear legal force, S hedged scope, R unclear reference, D implicit
-- default, G goal and means differ).
CREATE TABLE unit_vague (
  unit_id  TEXT NOT NULL REFERENCES unit_tag(unit_id),
  position INTEGER NOT NULL,
  code     TEXT NOT NULL CHECK (code IN ('J', 'M', 'S', 'R', 'D', 'G')),
  span     TEXT NOT NULL,
  PRIMARY KEY (unit_id, position)
);

-- Stage 3, selection. The paragraphs (text or figure) a topic's extraction reads, in handbook
-- order, each with the passage id the extraction prompt shows ('p17').
--   tag     it holds a sentence tagged with the topic, or is a figure tagged with it
--   lead    the lead paragraph of a selected list item ("Here are the steps for passing a vehicle:")
--   manual  added by a person
CREATE TABLE selection (
  run_id   TEXT NOT NULL REFERENCES run(id),
  position INTEGER NOT NULL,
  unit_id  TEXT NOT NULL REFERENCES unit(id),
  local_id TEXT NOT NULL,
  reason   TEXT NOT NULL CHECK (reason IN ('tag', 'lead', 'manual')),
  PRIMARY KEY (run_id, position),
  UNIQUE (run_id, local_id),
  UNIQUE (run_id, unit_id)
);

-- Statements ---------------------------------------------------------------------------------

CREATE TABLE statement (
  id            TEXT PRIMARY KEY,           -- 'mto:3.1.2a'; 'on-passing-1:p17a' for a run that is not a rules.json
  run_id        TEXT NOT NULL REFERENCES run(id),
  jurisdiction  TEXT NOT NULL,
  local_id      TEXT NOT NULL,              -- '3.1.2a', as in rules.json, or as the extraction wrote it
  position      INTEGER NOT NULL,           -- order in rules.json or in the extraction's output
  topic         TEXT NOT NULL,              -- 'passing'
  section       TEXT,
  type          TEXT NOT NULL,
  strength      TEXT,                       -- 'LAW', 'ADVICE' or NULL
  strength_from TEXT,
  text          TEXT NOT NULL,
  note          TEXT
);

CREATE TABLE statement_step (
  statement_id TEXT NOT NULL REFERENCES statement(id),
  n            TEXT NOT NULL,               -- '1', '2', ... or 'IF'
  position     INTEGER NOT NULL,
  text         TEXT NOT NULL,
  PRIMARY KEY (statement_id, position)
);

-- The statement (or step) split at its keywords: HEAD, then each modal and clause in order.
CREATE TABLE statement_part (
  statement_id TEXT NOT NULL REFERENCES statement(id),
  step         INTEGER,                     -- statement_step.position, or NULL for the statement line
  position     INTEGER NOT NULL,
  keyword      TEXT NOT NULL,               -- 'HEAD', 'MUST NOT', 'WHEN', 'IF VIOLATED', ...
  text         TEXT NOT NULL
);

CREATE TABLE statement_source (
  statement_id TEXT NOT NULL REFERENCES statement(id),
  position     INTEGER NOT NULL,
  unit_id      TEXT NOT NULL REFERENCES unit(id),   -- a passage, or a sentence or figure of its run's selection
  quote        TEXT,
  where_text   TEXT,
  census_id    TEXT,
  image        TEXT,
  PRIMARY KEY (statement_id, position)
);

CREATE TABLE step_source (
  statement_id TEXT NOT NULL,
  step         INTEGER NOT NULL,
  position     INTEGER NOT NULL,
  unit_id      TEXT NOT NULL REFERENCES unit(id),
  PRIMARY KEY (statement_id, step, position),
  FOREIGN KEY (statement_id, step) REFERENCES statement_step(statement_id, position)
);

-- EXCEPTION TO, SPECIALIZES, or a plain reference.
CREATE TABLE statement_link (
  from_id  TEXT NOT NULL REFERENCES statement(id),
  position INTEGER NOT NULL,
  to_id    TEXT NOT NULL REFERENCES statement(id),
  kind     TEXT NOT NULL CHECK (kind IN ('EXCEPTION TO', 'SPECIALIZES', 'REFERS TO')),
  PRIMARY KEY (from_id, position)
);

CREATE TABLE statement_figure (
  statement_id TEXT NOT NULL REFERENCES statement(id),
  position     INTEGER NOT NULL,
  unit_id      TEXT NOT NULL REFERENCES unit(id),   -- the passage that holds the figure
  figure       TEXT NOT NULL,               -- 'Diagram 2-46'
  PRIMARY KEY (statement_id, position)
);

-- The law behind a statement, and how the statement compares with it.
--   SAME       the provision states the same duty
--   BROADER    the statement applies in more cases than the provision (it drops a condition)
--   NARROWER   the statement applies in fewer cases than the provision
--   DIFFERENT  the statement and the provision disagree
--   PENALTY    the provision sets the statement's penalty
CREATE TABLE statement_basis (
  statement_id TEXT NOT NULL REFERENCES statement(id),
  unit_id      TEXT NOT NULL REFERENCES unit(id),
  relation     TEXT NOT NULL CHECK (relation IN ('SAME', 'BROADER', 'NARROWER', 'DIFFERENT', 'PENALTY')),
  note         TEXT,
  PRIMARY KEY (statement_id, unit_id)
);

-- The law added under a statement, which itself stays as extracted (its text, strength and
-- flags are the reference the extraction is scored against). Each line states, in the rule
-- language, what the law says on the statement's subject: the same duty, the duty the handbook
-- words as advice, the law's own definitions, conditions and exceptions, or its penalty. A word the
-- law leaves as open as the handbook keeps its [?…] mark.
CREATE TABLE statement_law (
  statement_id  TEXT NOT NULL REFERENCES statement(id),
  position      INTEGER NOT NULL,
  text          TEXT NOT NULL,
  note          TEXT,
  PRIMARY KEY (statement_id, position)
);

-- The provisions one added law line cites; each is also a statement_basis row of its statement,
-- which says how the statement compares with it.
CREATE TABLE statement_law_ref (
  statement_id  TEXT NOT NULL,
  position      INTEGER NOT NULL,
  unit_id       TEXT NOT NULL REFERENCES unit(id),
  PRIMARY KEY (statement_id, position, unit_id),
  FOREIGN KEY (statement_id, position) REFERENCES statement_law(statement_id, position)
);

-- Rule language ------------------------------------------------------------------------------

-- Every keyword, modal, flag code, verb, role, unit and fixed phrase of analysis/rule-language.md.
CREATE TABLE vocabulary (
  kind     TEXT NOT NULL,                   -- type, modal, clause, connective, link, procedure, define,
                                            -- action, flag, verb, role, unit, comparator, phrase
  word     TEXT NOT NULL,
  meaning  TEXT,
  modality TEXT,                            -- modals: obligation, prohibition, permission
  strength TEXT,                            -- modals: LAW or ADVICE
  section  TEXT,                            -- where rule-language.md defines it
  PRIMARY KEY (kind, word)
);

-- Flags and their grounding --------------------------------------------------------------------

-- A flagged word or phrase, per jurisdiction: 'on:safely'.
CREATE TABLE term (
  id           TEXT PRIMARY KEY,
  jurisdiction TEXT NOT NULL,
  phrase       TEXT NOT NULL
);

-- One flag of one statement (rule language §8).
CREATE TABLE occurrence (
  id           TEXT PRIMARY KEY,            -- 'mto:3.1.2a|R|30 m from'
  statement_id TEXT NOT NULL REFERENCES statement(id),
  position     INTEGER NOT NULL,            -- order among the statement's flags
  code         TEXT NOT NULL,               -- J S R G M D V X
  span         TEXT NOT NULL,
  note         TEXT,
  note_zh      TEXT,
  term_id      TEXT REFERENCES term(id)
);

-- Resolving one flag (stage 5): the verdict, after searching the rest of the handbook and the law.
--   RESOLVED  a source settles it for every case the statement covers
--   PARTIAL   settled only for some cases, or narrowed but not settled
--   OPEN      nothing settles it
CREATE TABLE grounding (
  occurrence_id TEXT PRIMARY KEY REFERENCES occurrence(id),
  verdict       TEXT NOT NULL CHECK (verdict IN ('RESOLVED', 'PARTIAL', 'OPEN')),
  definition    TEXT,                       -- the reading that resolves it, for the cases it covers
  effect        TEXT,                       -- what it would change in the statement
  note          TEXT
);

-- What each kind of source says about the flagged words: the rest of the handbook, the law, and an
-- engineering standard or safety model where one was consulted (a proxy, not law).
--   DEFINES   a definition, number, measure or test that makes the words checkable
--   STATES    settles it without a measure: makes it a duty or not, names the referent, says the
--             default, shows two words name one thing, or states the same rule in agreeing words
--   REPEATS   the same open words, or equally open ones
--   SILENT    nothing on it
CREATE TABLE grounding_finding (
  occurrence_id TEXT NOT NULL REFERENCES grounding(occurrence_id),
  side          TEXT NOT NULL CHECK (side IN ('handbook', 'law', 'standard')),
  finding       TEXT NOT NULL CHECK (finding IN ('DEFINES', 'STATES', 'REPEATS', 'SILENT')),
  says          TEXT,                       -- what that side says about the words, in a sentence
  PRIMARY KEY (occurrence_id, side)
);

-- The sentences and provisions behind the findings; role 'standard' and 'model' are the standard side.
CREATE TABLE grounding_link (
  occurrence_id TEXT NOT NULL REFERENCES grounding(occurrence_id),
  unit_id       TEXT NOT NULL REFERENCES unit(id),
  role          TEXT NOT NULL CHECK (role IN ('law', 'standard', 'model', 'handbook')),
  PRIMARY KEY (occurrence_id, unit_id)
);

-- Views ----------------------------------------------------------------------------------------

-- Each handbook sentence (Ontario) or paragraph, with the statements that cite it: through a
-- passage, directly as a sentence (and so its paragraph), or as a whole paragraph (and so its sentences).
CREATE VIEW unit_use AS
  WITH cited AS (SELECT statement_id, unit_id FROM statement_source UNION SELECT statement_id, unit_id FROM step_source)
  SELECT pp.part_id AS unit_id, c.statement_id FROM cited c JOIN passage_part pp ON pp.passage_id = c.unit_id
  UNION
  SELECT u.id, c.statement_id FROM cited c JOIN unit u ON u.id = c.unit_id WHERE u.kind IN ('paragraph', 'sentence')
  UNION
  SELECT u.parent_id, c.statement_id FROM cited c JOIN unit u ON u.id = c.unit_id WHERE u.kind = 'sentence'
  UNION
  SELECT x.id, c.statement_id FROM cited c JOIN unit x ON x.parent_id = c.unit_id WHERE x.kind = 'sentence';

-- For each extraction run, the sentences and figures tagged with its topic that none of its
-- statements cites.
CREATE VIEW topic_unit_unused AS
  SELECT r.id AS run_id, u.id, u.locator, u.text
  FROM run r JOIN unit u ON u.source_id = r.source_id JOIN unit_topic t ON t.unit_id = u.id AND t.topic = r.topic
  WHERE r.stage = 'extract'
    AND NOT EXISTS (SELECT 1 FROM unit_use x JOIN statement s ON s.id = x.statement_id
                    WHERE x.unit_id = u.id AND s.run_id = r.id);

-- Topic passages that no statement or step cites.
CREATE VIEW passage_unused AS
  SELECT u.id, u.source_id, u.locator, u.text
  FROM unit u
  WHERE u.kind = 'passage'
    AND u.id NOT IN (SELECT unit_id FROM statement_source UNION SELECT unit_id FROM step_source
                     UNION SELECT unit_id FROM statement_figure);

-- Flags with no grounding yet.
CREATE VIEW ungrounded_flag AS
  SELECT o.id, s.run_id, s.jurisdiction, o.code, o.span, s.text
  FROM occurrence o JOIN statement s ON s.id = o.statement_id
  WHERE o.id NOT IN (SELECT occurrence_id FROM grounding);

-- LAW statements that cite no provision other than a penalty.
CREATE VIEW law_without_basis AS
  SELECT s.id, s.run_id, s.jurisdiction, s.text
  FROM statement s
  WHERE s.strength = 'LAW'
    AND NOT EXISTS (SELECT 1 FROM statement_basis b WHERE b.statement_id = s.id AND b.relation != 'PENALTY');

-- ADVICE statements with a provision of a statute or regulation behind them: candidates for LAW.
CREATE VIEW advice_with_law AS
  SELECT s.id AS statement_id, s.run_id, s.jurisdiction, b.unit_id, b.relation, b.note, s.text
  FROM statement s
  JOIN statement_basis b ON b.statement_id = s.id
  JOIN unit u ON u.id = b.unit_id
  JOIN source src ON src.id = u.source_id
  WHERE s.strength = 'ADVICE' AND b.relation IN ('SAME', 'BROADER', 'NARROWER')
    AND src.kind IN ('statute', 'regulation');

-- Statements with a provision of a statute or regulation behind them (other than a penalty) and
-- no law line added yet.
CREATE VIEW law_not_added AS
  SELECT DISTINCT s.id, s.run_id, s.jurisdiction, s.strength, s.text
  FROM statement s
  JOIN statement_basis b ON b.statement_id = s.id
  JOIN unit u ON u.id = b.unit_id
  JOIN source src ON src.id = u.source_id
  WHERE b.relation != 'PENALTY' AND src.kind IN ('statute', 'regulation')
    AND s.id NOT IN (SELECT statement_id FROM statement_law);
