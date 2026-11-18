## Your task

Review the rule given below this task. Find everything wrong with it, if anything: anything that
makes it unfaithful to the handbook blocks shown, incomplete, misleading, ambiguous, or not in the
form the extractor's instructions require.

Do not work through a fixed checklist; look for any error. Ask, for example:

- Does the handbook, in the cited blocks, really say this, in this situation, for this actor?
- Is anything added that the handbook does not say, or left out that it does say in these blocks?
- Is the strength the handbook's own?
- Would a driving model reading only this rule understand exactly what to do, and when?
- Are the citations the blocks that support the rule: all of them, and only them?
- Does the rule follow the extractor's instructions to the letter: the grammar, the fields, force
  and modal, citations, vague terms, the note?
- Is every term written and used as the instructions and the vocabulary require? Go through the
  rule's words: a word or phrase naming a vocabulary term with its defined meaning should be in
  CAPITALS; a word in CAPITALS should mean exactly what its vocabulary entry defines; a lowercase
  phrase that looks like a vocabulary term but means something else invites misreading; a key term
  that needs a strict definition should be a defined term.

Report only problems of this rule, or of a vocabulary entry as this rule uses it, not problems of
other rules.

## Each finding

- `title`: a short heading that states the error, such as "A night-only step is applied to every
  pass" or "BLIND SPOT is used but not in the vocabulary".
- `category`: a short name for the kind of error, such as "citation", "strength" or "vocabulary".
- `severity`: `major` when the error changes what the rule tells a driver to do, or when, or who it
  applies to, or its strength, or leaves the rule without support; `minor` for wording, format,
  clarity or citation precision that does not change the rule's meaning.
- `description`: what is wrong and why, in plain prose. Quote the rule's words at fault, and quote
  the handbook passages that show the error as `id`: "text" (trim with "…"), so a reader can check
  the finding without opening the handbook.
- `suggested_fix`: how to fix it, in whatever form fits: the corrected text of the fields to change,
  a split into several rules (each written out), a vocabulary entry to add or change, citations to
  add or remove, or a note to add. Write corrected text out in full rather than describing it.
- `confidence`: `high`, `medium` or `low`: how sure you are that this is an error.

One problem per finding. When the rule has no errors, answer with an empty `findings` list.

Answer with JSON only.
