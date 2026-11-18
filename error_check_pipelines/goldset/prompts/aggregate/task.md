## Your task

Review the rule set above against the whole handbook, for the topic named in the extractor's
instructions only. Find everything wrong with the set as a whole, if anything. Look for two kinds
of error above all, and report any other error of the set you find.

**Coverage.** Go through the handbook, every page and not only the pages the rules cite, and find
what the handbook states about the topic that the set does not capture. Ask, for example:

- Is there a rule, condition, exception, penalty, diagram or sign about the topic that no rule
  states?
- Is a rule stated in several places, and does the set cite and use only some of them: a passage
  elsewhere that words it more strongly, adds a condition or exception, or gives a penalty?
- Does a passage elsewhere narrow, extend or contradict what a rule says?
- Is a vocabulary term the set defines itself actually defined in the handbook, or a vague term
  actually quantified somewhere?

Stay within the topic: report a missing rule only when it is about the topic as the extractor's
instructions name it. When a case is on the boundary of the topic, say so and give your
confidence.

**Conflicts.** Read the rules against each other. Ask, for example:

- Do two rules tell the same actor, in the same situation, to do incompatible things, or does one
  forbid what another requires or allows?
- Does an exception in one rule clash with another rule, or does one rule's condition overlap
  another's so that it is unclear which applies?
- Do two rules say the same thing (duplicates), or does one rule wrongly repeat part of another?
- Is the same thing named with different words, or the same word used with different meanings,
  across rules? Is a vocabulary term used in a way its definition does not fit?
- Are similar handbook wordings given different strengths, or similar cases split into rules at
  very different levels of detail?
- Do notes or cross-references between rules point to the wrong rule or say something another
  rule contradicts?

Report each problem once, naming every rule it involves.

## Each finding

- `kind`: `coverage` for something the set leaves out or under-uses from the handbook, `conflict`
  for a problem between rules, `other` for any other error of the set.
- `rules`: the ids of the rules the finding involves, or `[]` when no rule covers the material.
- `title`: a short heading that states the error, such as "A sign that forbids passing is not
  covered" or "Two rules give the same driver opposite instructions in the same situation".
- `category`: a short name for the kind of error, such as "missing rule", "missing citation",
  "contradiction", "duplicate" or "inconsistent terms".
- `severity`: `major` when the error changes what the rule set tells a driver to do, or when, or
  who it applies to, or its strength, or leaves out a rule of the topic; `minor` for wording,
  citation, consistency or clarity problems that do not change what a driver should do.
- `description`: what is wrong and why, in plain prose. Quote the rules' words at fault, and quote
  the handbook passages that show the error as `id`: "text" (trim with "…"), so a reader can check
  the finding without opening the handbook.
- `suggested_fix`: how to fix it, in whatever form fits: a new rule written out in full with all
  its fields, the corrected text of the fields to change, rules to merge or split (each written
  out), a vocabulary entry to add or change, citations to add or remove, or a note to add.
- `confidence`: `high`, `medium` or `low`: how sure you are that this is an error.

One problem per finding. When the set has no errors, answer with an empty `findings` list.

Answer with JSON only.
