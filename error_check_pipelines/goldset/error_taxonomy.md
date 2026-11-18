# Error taxonomy

Kinds of errors found in extracted rules: a record for triage and analysis. **It is not given to the
check judges** (stages 2 and 3), so the checks stay the same across runs. The list is not complete.

At triage, the free-form category the judge gave each confirmed finding is mapped to a category
here, or a new category is added, with examples from confirmed findings.

## Categories

- **Faithfulness**: the rule says something the handbook does not, or contradicts it: wrong
  situation, wrong action, added facts.
- **Conditions and exceptions**: a condition or exception the handbook states is missing, or one is
  added that it does not state.
- **Actor**: the rule applies to the wrong road user, or is too broad or too narrow.
- **Strength**: force or modal differ from the handbook's wording: advice turned into an obligation,
  an obligation softened, a prohibition turned into a permission.
- **Citation**: a cited block does not support the rule, or a block that supports it is not cited
  (the passage, its exception, its diagram or caption).
- **Terminology and vocabulary**: a defined term used with a different meaning from its definition;
  a key term that should be a defined term but is not; a definition that does not fit the handbook.
- **Clarity and ambiguity**: the rule can be read more than one way.
- **Vagueness**: a vague word from the handbook is not listed in `vague_terms`; a listed term is not
  vague; a number or definition was made up to replace the handbook's vague wording.
- **Scope**: the rule is not about the topic, or is not a rule (an explanation, a reason, a
  statistic).
- **Granularity**: one rule split into pieces, or separate rules for different situations merged
  into one.
- **Note**: the note is wrong, or is missing something a checker needs (a rule inferred from two
  places, a rule resting on a diagram, stronger wording chosen).

## Conventions (decided at triage; findings against these are rejected)

- The verb "pass" is written in lowercase ("the DRIVER MAY pass"). Only the noun PASS is capitalized,
  as in the extraction prompt's example.
- A term defined in the vocabulary is not defined or mentioned again in a rule's note.
- Rule titles are not part of the grammar and may use lowercase for defined terms.
- A rule's action may join a positive and a negative part ("allow more room before moving back and
  not cut back into the lane too soon") when the negation is unambiguous.
