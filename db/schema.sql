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

-- Every citable piece of a document, verbatim.
--   paragraph  a handbook paragraph, list item, step or figure (analysis/segments/)
--   sentence   one sentence of a paragraph (Ontario only, from the census)
--   passage    a passage chosen for a topic (inputs/); it covers sentences or paragraphs
--   provision  a subsection or clause of a law or regulation, or a part of a standard
CREATE TABLE unit (
  id        TEXT PRIMARY KEY,               -- 'mto:para:driving-along:018', 'mto:sent:index:001.1', 'mto:passage:m17', 'on-hta:148(8)'
  source_id TEXT NOT NULL REFERENCES source(id),
  kind      TEXT NOT NULL CHECK (kind IN ('paragraph', 'sentence', 'passage', 'provision')),
  parent_id TEXT REFERENCES unit(id),       -- a sentence's paragraph
  page      TEXT,                           -- handbook page file, without .html
  locator   TEXT NOT NULL,                  -- 'Driving along › Maintaining space · ¶2', 's. 148 (8)'
  heading   TEXT,                           -- a provision's marginal heading
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

-- The census label of each Ontario sentence (analysis/census/census-guidelines.md).
CREATE TABLE sentence_label (
  unit_id TEXT PRIMARY KEY REFERENCES unit(id),
  type    TEXT,                             -- RULE, FACT, DEFINE, STEP, CONSEQ, META
  role    TEXT,
  modal   TEXT,
  basis   TEXT,                             -- where its legal strength comes from
  caution INTEGER,
  fit     TEXT,                             -- how well the first grammar draft could write it
  passing INTEGER,                          -- 1 if it is about passing
  rewrite TEXT
);

-- The words the census pulled out of each sentence: action, entities, situation dimensions,
-- vague words, clause keywords, and what the first grammar draft lacked.
CREATE TABLE sentence_word (
  unit_id  TEXT NOT NULL REFERENCES unit(id),
  kind     TEXT NOT NULL CHECK (kind IN ('action', 'entity', 'dimension', 'vague', 'clause', 'need')),
  position INTEGER NOT NULL,
  word     TEXT NOT NULL,
  code     TEXT,                            -- a vague word's flag code (rule language §8)
  PRIMARY KEY (unit_id, kind, position)
);

-- Statements ---------------------------------------------------------------------------------

CREATE TABLE statement (
  id            TEXT PRIMARY KEY,           -- 'mto:3.1.2a'
  jurisdiction  TEXT NOT NULL,
  local_id      TEXT NOT NULL,              -- '3.1.2a', as in rules.json
  position      INTEGER NOT NULL,           -- order in rules.json
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
  unit_id      TEXT NOT NULL REFERENCES unit(id),   -- a passage
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

-- How far a formal source settles one flag.
--   LAW_DEFINES  the law gives the definition or the number
--   LAW_STATES   the law states the duty itself, which settles its strength, scope or reference
--   LAW_REPEATS  the law uses the same open word; the vagueness is in the law too
--   STANDARD     the law leaves it open and an engineering standard or safety model gives an
--                operational definition (a proxy, not law)
--   HANDBOOK     another part of the handbook settles it
--   OPEN         no formal source settles it
CREATE TABLE grounding (
  occurrence_id TEXT PRIMARY KEY REFERENCES occurrence(id),
  status        TEXT NOT NULL CHECK (status IN ('LAW_DEFINES', 'LAW_STATES', 'LAW_REPEATS', 'STANDARD', 'HANDBOOK', 'OPEN')),
  definition    TEXT,                       -- the measurable reading, when there is one
  effect        TEXT,                       -- what it would change in the statement
  note          TEXT
);

CREATE TABLE grounding_link (
  occurrence_id TEXT NOT NULL REFERENCES grounding(occurrence_id),
  unit_id       TEXT NOT NULL REFERENCES unit(id),
  role          TEXT NOT NULL CHECK (role IN ('law', 'standard', 'model', 'handbook')),
  PRIMARY KEY (occurrence_id, unit_id)
);

-- Views ----------------------------------------------------------------------------------------

-- Each handbook sentence (Ontario) or paragraph, with the statements that cite it.
CREATE VIEW unit_use AS
  SELECT pp.part_id AS unit_id, s.statement_id FROM passage_part pp JOIN statement_source s ON s.unit_id = pp.passage_id
  UNION
  SELECT pp.part_id, s.statement_id FROM passage_part pp JOIN step_source s ON s.unit_id = pp.passage_id;

-- Ontario sentences the census marked as about passing that no statement cites.
CREATE VIEW passing_sentence_unused AS
  SELECT u.id, u.locator, u.text
  FROM unit u JOIN sentence_label l ON l.unit_id = u.id
  WHERE l.passing = 1 AND u.id NOT IN (SELECT unit_id FROM unit_use);

-- Topic passages that no statement or step cites.
CREATE VIEW passage_unused AS
  SELECT u.id, u.source_id, u.locator, u.text
  FROM unit u
  WHERE u.kind = 'passage'
    AND u.id NOT IN (SELECT unit_id FROM statement_source UNION SELECT unit_id FROM step_source
                     UNION SELECT unit_id FROM statement_figure);

-- Flags with no grounding yet.
CREATE VIEW ungrounded_flag AS
  SELECT o.id, s.jurisdiction, o.code, o.span, s.text
  FROM occurrence o JOIN statement s ON s.id = o.statement_id
  WHERE o.id NOT IN (SELECT occurrence_id FROM grounding);

-- LAW statements that cite no provision other than a penalty.
CREATE VIEW law_without_basis AS
  SELECT s.id, s.jurisdiction, s.text
  FROM statement s
  WHERE s.strength = 'LAW'
    AND NOT EXISTS (SELECT 1 FROM statement_basis b WHERE b.statement_id = s.id AND b.relation != 'PENALTY');

-- ADVICE statements with a provision of a statute or regulation behind them: candidates for LAW.
CREATE VIEW advice_with_law AS
  SELECT s.id AS statement_id, s.jurisdiction, b.unit_id, b.relation, b.note, s.text
  FROM statement s
  JOIN statement_basis b ON b.statement_id = s.id
  JOIN unit u ON u.id = b.unit_id
  JOIN source src ON src.id = u.source_id
  WHERE s.strength = 'ADVICE' AND b.relation IN ('SAME', 'BROADER', 'NARROWER')
    AND src.kind IN ('statute', 'regulation');

-- Statements with a provision of a statute or regulation behind them (other than a penalty) and
-- no law line added yet.
CREATE VIEW law_not_added AS
  SELECT DISTINCT s.id, s.jurisdiction, s.strength, s.text
  FROM statement s
  JOIN statement_basis b ON b.statement_id = s.id
  JOIN unit u ON u.id = b.unit_id
  JOIN source src ON src.id = u.source_id
  WHERE b.relation != 'PENALTY' AND src.kind IN ('statute', 'regulation')
    AND s.id NOT IN (SELECT statement_id FROM statement_law);
