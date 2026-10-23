# Score: provenance/fixed-v1-check/signs/output.json against the 6 reference statements whose sources are all on the Signs page (reference-signs.json)

## Summary

- Statements: model 8 (DEFINE 1, FACT 1, RULE 6); reference 6 (DEFINE 1, RULE 5).
- Paired by shared sources: 6. Reference recall 6/6 (100%); model precision 6/8 (75%).
- On paired statements: type 6/6 (100%), force 6/6 (100%), modal 6/6 (100%), clause keywords 6/6 (100%), same sources 5/6 (83%), links 6/6 (100%).
- Law or advice on paired rules and procedures: 5/5 (100%).
- Inline flags (J, S, R, G) on paired statements: precision 0.20, recall 1.00, F1 0.33; same code on 1 of 1 matched spans.
- Passages the reference cites and the model does not: none.
- Passages the model cites and the reference does not: none.

## Validity

- Schema errors: 0
- Duplicate ids: none; links to missing ids: none; unknown source ids: none.
- Quotes that are not the full passage text: 0.
- Statements using "you": none.
- Capitalised words that are not keywords: none.
- Numbers not found in the sources: none.

## Hard cases

| Case | Reference statements | Paired | Clauses, modal and force agree | Not paired |
|---|---|---|---|---|
| condition only in a heading | 15 | 3 | 3 | 3.2.2a 3.3.1b 3.3.2a 3.3.2b 3.3.3a 3.3.3b 3.4.4a 3.4.4c 3.4.5d 3.4.7a 3.4.8a 3.5.2a |
| condition only in a neighbouring passage | 2 | 0 | 0 | 2.2b 3.1.4a |
| legal force set only by a heading | 3 | 2 | 2 | 3.6.1c |
| link between different passages | 3 | 0 | 0 | 2.2b 3.3.1b 3.4.12e |
| duty written apart from its penalty | 4 | 0 | 0 | 3.4.4b 3.4.12b 3.4.13a 3.4.13b |
| sources on two pages | 6 | 0 | 0 | 3.1.1a 3.4.13a 3.4.13b 3.6.1a 3.6.3a 3.6.3b |

Passages that should give no passing rule (m92 to m96) cited by the model: none.

## Paired statements that disagree

| Reference | Model | Differs in | Reference text | Model text |
|---|---|---|---|---|

## Reference statements with no pair

- none

## Model statements with no pair

- m68a (FACT, sources m67, m68): FACT a "long" placard indicates a long commercial vehicle
- m68c (RULE, sources m67, m68): a driver SHOULD be able to recognize a long commercial vehicle on the highway by the rear signage of the long commercial vehicle
