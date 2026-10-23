# Rule template plan (draft v0, for discussion)

> Superseded by `rule-language-v1.md`, which was settled from the full-handbook census (`census/census-report.md`). Kept for the reasoning and the prior-work table.

Goal: write the MTO Driver's Handbook as a **minimal, natural-language-like rule language**. The keyword set should be small and fixed, like SQL's. It should read easily for an LLM/VLM, and every rule should trace back to the original text.

Contents:
1. Design principles
2. Draft grammar v0 (with passing examples)
3. How to arrive at a minimal set (full-handbook census + coverage curve)
4. Flagging vague content
5. Prior work: what to borrow
6. Overall pipeline and evaluation
7. Decisions to discuss

---

## 1. Design principles

1. **Small, closed keyword set.** Every keyword has exactly one meaning. Don't add a keyword when composing existing ones will do (SQL: SELECT/WHERE/JOIN cover most queries).
2. **Natural-language body, controlled frame.** The keywords are fixed, and conditions and actions read as English. The vocabulary is closed too: one phrase per concept. (Logical English lesson: "drives in a lane", "travels in a lane" and "is driving on a carriageway" all collapse into one predicate.)
3. **Keep vague content as it is; don't invent thresholds.** "safe" and "enough" stay as written and get a marker. They are resolved in a later step.
4. **Every rule carries a source.** A verbatim quote plus page#section, so that human verification only checks the quote and the rewrite.
5. **Legal force and advice are separate.** The handbook mixes legal obligations (HTA) with good-driver advice, and the two must not be mixed in rules.

---

## 2. Draft grammar v0

### 2.1 Statement types (4)

| Type | Pattern | Holds |
|---|---|---|
| **DEFINE** | `DEFINE <term> IS <genus> THAT <differentia> [ALSO CALLED <alias>]` | Definitions, vocabulary |
| **FACT** | `FACT <subject> <is/has/...> <...>` | Background facts, road facilities, sign meanings (no instruction) |
| **RULE** | `<role> <MODAL> <action> [clauses]` | Obligations, prohibitions, permissions, advice, cautions |
| **PROCEDURE** | `TO <goal>: STEP 1 …; STEP n …; DONE WHEN <cond>; IF <event> THEN <fallback>` | Ordered steps |

### 2.2 Modals (closed set, 5)

| Modal | Meaning | Force |
|---|---|---|
| `MUST` / `MUST NOT` | Obligation / prohibition | LEGAL |
| `MAY` | Permission (often paired with ONLY IF) | LEGAL |
| `SHOULD` / `SHOULD NOT` | Advice / good-driver practice | ADVISORY |

Cautions are written as `SHOULD WATCH FOR <hazard>`. They aren't a separate type, which saves one keyword (see decision 1).

### 2.3 Clauses (shared by every statement, like SQL's WHERE)

| Clause | Meaning | Source |
|---|---|---|
| `WHEN <situation/event>` | Applicability condition (trigger) | EARS |
| `WHILE <ongoing state>` | Holds for a period (e.g. while passing, while being passed) | EARS |
| `ONLY IF <cond>` | Necessary condition for a MAY | RuleSpeak |
| `UNLESS <cond>` | Exception within the same sentence | — |
| `BECAUSE <reason>` | Reason | — |
| `IF VIOLATED <penalty>` | Fine, demerit points, suspension | L4 `LEST`, LegalRuleML Reparation |
| `AND` / `OR` / `NOT` | Connectives; AND binds tighter than OR | ACE fixed interpretation rules |

### 2.4 Links between rules (header attributes, not new statements)

- `EXCEPTION TO <id>`: an exception from a different passage (Catala default/exception)
- `SPECIALIZES <id>`: a variant (e.g. passing at night specializes passing)

### 2.5 Metadata (every statement)

`ID` · `SOURCE "<verbatim quote>" @ <page>#<section>` · `TAGS <situation dimensions>` (place / road / time-weather / object being passed / role)

**Total: about 20 keywords** (DEFINE IS THAT ALSO-CALLED, FACT, TO STEP DONE-WHEN IF-THEN, MUST, MUST NOT, MAY, SHOULD, SHOULD NOT, WHEN, WHILE, ONLY IF, UNLESS, BECAUSE, IF VIOLATED, AND/OR/NOT, EXCEPTION TO, SPECIALIZES).

Entity references follow Logical English: introduce with `a <entity>`, then refer back with `the <entity>`. This matters for passing, where "the vehicle you are passing" has to stay the same vehicle through every step (Scene Flow Specifications: 20% of rules need the same entity tracked across time).

### 2.6 Passing examples (`[?…]` marks vague content, see §4)

```
DEFINE passing IS a lane change THAT moves past a slower vehicle.

RULE P1  a driver MUST NOT pass a vehicle UNLESS the driver is [?sure] the pass is without danger to anyone.
RULE P2  a driver SHOULD NOT pass a vehicle WHEN the driver is [?in doubt].
RULE P3  a driver [?MUST NOT] pass a snow plow WHEN the snow plow is moving.          -- "Don't … under any conditions": law or advice?
RULE P4  a driver MUST NOT pass a vehicle WHEN the driver is within 30 m of a pedestrian crossover.
RULE P5  a driver MUST NOT pass on the left of the centreline WHEN the driver is within 30 m of a bridge, viaduct or tunnel.
RULE P6  a driver SHOULD NOT pass WHEN (approaching a hill crest OR on a curve)
           AND the view of oncoming traffic is obstructed AND the clear distance ahead is not [?enough] to pass [?safely].
RULE P7  a driver SHOULD WATCH FOR doors opening suddenly WHILE the driver passes a parked vehicle.
RULE P8  a driver [?MUST NOT] pass a two-wheeler within the two-wheeler's lane
           BECAUSE two-wheelers often move within their lane to avoid hazards or to be seen.

TO pass a vehicle:
  STEP 1 signal left AND check that the way is clear ahead and behind; move into the passing lane.
  STEP 2 WATCH FOR hidden bicycles and small vehicles ahead of the vehicle, vehicles turning left ahead, and entering vehicles or pedestrians.
  STEP 3 signal right.
  DONE WHEN the entire front of the vehicle is visible in the inside mirror → return to the original lane.
  IF the vehicle speeds up THEN do not race AND return to the original lane.

RULE B1  a driver being passed MUST NOT speed up WHILE another driver is passing the driver.   -- the text says "unlawful"
RULE B2  a driver being passed SHOULD move right WHEN faster traffic wants to pass.

RULE S1  a driver MAY drive on the right shoulder ONLY IF the driver is passing a left-turning vehicle AND the shoulder is paved.
RULE S2  a driver MUST NOT pass on the left shoulder.
RULE R0  a driver SHOULD pass on the left.                                       -- "Most passing is done on the left": a default, not a rule?
RULE R1  EXCEPTION TO R0: a driver MAY pass on the right WHEN the road is multi-lane OR one-way
           OR the vehicle is a streetcar OR the vehicle is turning left.
RULE T1  a driver MUST pass a streetcar on the right UNLESS the road is one-way.

TO pass a vehicle at night  SPECIALIZES "TO pass a vehicle"  TAGS time=night:
  STEP 1 switch to low beams WHILE approaching the vehicle from behind. …

FACT [?many] high-speed roads with 3+ lanes each way bar trucks from the far-left lane.
FACT the lane next to the far-left lane is the truck passing lane.
```

Problems that show up in this exercise (these are where the discussion should go):
- **Imperatives ("move to the right", "Don't …") don't say whether they're law or advice.** This is the most common case in the handbook, so a default rule is needed (decision 2).
- The modality of P3 and P8 is unclear from the text alone, so they're flagged rather than guessed.
- "Trucks are not allowed in the far-left lane" is actually a rule for the **truck driver**, so the role isn't always the reader.

---

## 3. How to arrive at a minimal set

You're right that the template set can only be settled after a full pass over the handbook. My suggestion is a **coverage-driven** approach (similar to the SFS paper, which went through all 207 Virginia sections and reported that 96% are expressible):

**Step 1: sentence-level census.** Split the handbook into sentences (my rough split gives **3,585**). An LLM labels each one with:
- content type (DEFINE / FACT / RULE / PROCEDURE / non-normative)
- which v0 pattern it fits, or NO-FIT
- ambiguity flags (§4)

A human spot-checks a sample.

**Step 2: coverage curve and admission rules.** Rank keywords by the share of sentences each covers. A keyword is admitted only if:
- (a) its NO-FIT cluster is big enough (e.g. ≥1% of normative sentences) or safety-critical, **and**
- (b) existing keywords can't compose it.

Keywords that are rarely used or redundant get removed. The output reports "% expressible + a list of what can't be expressed" (e.g. catch-all clauses like "reckless driving").

**Step 3: freeze grammar v1 + lexicon.** The lexicon holds roles (driver, driver being passed, truck driver …), entities (vehicle, lane, shoulder …) and actions (pass, change lanes, signal …), one phrase per concept.

**Rough evidence from my regex scan** (keyword matching only, which over-counts; e.g. "can" is sometimes ability, not permission):

| Marker | Sentences |
|---|---|
| must / required | 317 |
| may / can (permission) | 213 |
| never / do not / don't | 194 |
| should | 108 |
| watch for / be careful / be prepared | 97 |
| avoid / try to | 82 |
| if / when conditions | 580 |
| unless / except | 38 |
| because / so that (reasons) | 71 |
| penalties (fine / demerit / suspension) | 110 |
| numeric thresholds (m, km/h, seconds) | 75 |
| contains a vague term (safe, enough, properly …) | **383 (~11%)** |
| no modal marker at all (descriptions, facts, headings, bare imperatives) | **1,967 (~55%)** |

Takeaways:
- FACT and bare imperatives make up a large share, so FACT can't be dropped, and the default modality for imperatives matters.
- Penalties appear 110 times, so `IF VIOLATED` is worth a keyword.
- `unless` appears only 38 times; whether to keep it inline is decision 3.

---

## 4. Flagging vague content

Inline marker `[?…]`, plus a **vagueness register** (one entry per term: category, occurrences, any concrete definition the handbook gives elsewhere, e.g. the 2-second rule). Treatment of each entry comes later. Proposed categories:

| Code | Category | Handbook example |
|---|---|---|
| J | Judgment term (open texture) | safe, enough, sure, in doubt, reasonable speed, plenty of room, as soon as you can |
| M | Unclear modality / legal force | "Don't pass moving snow plows", "Do not take this as an invitation to pass" |
| S | Hedged scope | "many high-speed roads", "most passing", "usually", "often" |
| R | Unclear reference or role | "these areas", "the lane next to it", truck vs your own car |
| D | Implicit default | the shoulder rule presupposes "you normally can't drive on the shoulder" |
| G | Goal vs sub-action mismatch | sometimes prohibits "passing", sometimes "crossing the centreline" (the LE paper raises the same issue) |
| V | Synonyms / vocabulary drift | passing / overtaking; inconsistent lists of two-wheeler types |
| X | Repeated across pages, possibly inconsistent | the 30 m crossover rule appears in both Changing positions and Stopping, worded differently |

Later treatment can draw on Rizaldi et al.: keep the vague term as a named predicate in the rule body, and put its operational definition in a separate, swappable definition entry. The rule text then never has to change.

---

## 5. Prior work: what to borrow

| Work | Borrow | Avoid |
|---|---|---|
| **EARS** (Mavin et al., RE'09) | Small fixed set of sentence openers; the WHEN (event) vs WHILE (state) split; IF…THEN for abnormal situations | Only SHALL; no permission, advice or exception |
| **RFC 2119** | MUST / SHOULD / MAY tiers | — |
| **RuleSpeak / SBVR** | `MAY … ONLY IF`; separate vocabulary (definitions) from behavioural rules; rules carry an enforcement level | SBVR metamodel is too heavy |
| **Logical English** (Kowalski; both LE papers in the Paper folder) | Closed predicate templates; a/the variable references; the predicate library grows with use | LE drops modal strength and has no advice tier |
| **Zin et al. 2025** (Prolog paper in the folder) | Human-in-the-loop expansion; LLMs struggle most where background must be filled in to resolve ambiguity, so flag those cases separately | Only 20 rules; LE→Prolog accuracy is 75% |
| **Sartor et al.** (Mind the Gaps, in the folder) | The UK Highway Code also splits MUST (law) from should/take extra care (advice), which supports separating LEGAL and ADVISORY | — |
| **Catala** (ICFP 2021) | Exceptions as separate statements naming the rule they override; two exceptions firing at once is reported as a conflict | Too code-like |
| **L4 / LegalRuleML** | Penalties attached to the rule (`LEST` / Reparation); priority/override relations | — |
| **Rulebooks** (Censi et al. 2019) + **Rulebook Flywheel** (TNO 2026, in the folder) | Rules have priorities; TNO's rule triple (key element, condition, desired behaviour, intention) is close to our RULE + BECAUSE | Non-binary metrics come later |
| **Scene Flow Specifications** (FSE 2025, in the folder) | A census over the whole code reporting % expressible; tracking the same entity across time | Its target is runtime monitoring, not an LLM |
| **Rizaldi et al.** (iFM 2017, overtaking rules in Isabelle) | Write rules abstractly first, then concretize vague terms separately | — |
| **Driving with Regulation** (Cai et al., AAAI-26) | Uses a driver's manual too; splits mandatory rules from safety guidelines at runtime, supporting a LEGAL/ADVISORY tag written into the rule at extraction | Leaves the split to the LLM at runtime |
| **TR2MTL** (IV 2024) | Uses an LLM to translate traffic rules into temporal logic (MTL) | The symbolic route we're avoiding |
| **Prakken 2017** (AI & Law) | Lists exceptions, conflicts, open texture and common sense as the core problems; resolves conflicts with lex specialis | — |

Not verified this time: the full keyword lists for SBVR, ACE and LegalRuleML (from memory); the details of how Maierhofer et al. (IV 2020) handle thresholds for vague terms (full text unavailable).

---

## 6. Overall pipeline and evaluation

1. **Census** (§3 Step 1) → grammar v1 + lexicon + vagueness register
2. **Pilot: passing.** Two-stage VLM: gather + classify (with source quotes), then fill templates. Compare against michael's artifact (80 passages from 15 pages).
3. **Full handbook.** Humans verify sources and classification only.
4. **Resolve the vagueness register** (by category: concretize, keep as judgment, or drop)

Evaluation metrics:
- **Coverage:** % of handbook sentences expressible
- **Faithfulness:** humans check quote ↔ rule; plus round-trip (rule → English, compared with the original)
- **Consistency:** two runs on the same passage produce the same rule
- **Downstream:** the handbook's "Test yourself – sample knowledge test questions" page. Have the LLM answer using (a) the original text vs (b) our rules. This is a direct test of the claim that a natural-language-like format suits LLM reasoning better, and could also be compared against an LTL version.

---

## 7. Decisions to discuss

1. **Is caution its own type?** I recommend folding it into `SHOULD WATCH FOR` for a smaller set; the cost is losing the "perception cue" category.
2. **Default modality for bare imperatives:** I recommend SHOULD (ADVISORY) by default, upgraded to MUST only when the text says illegal / not permitted / must, or HTA backs it. Everything else gets an M flag.
3. **Exceptions: inline UNLESS or separate EXCEPTION TO?** I recommend both: UNLESS within the same sentence, EXCEPTION TO across passages.
4. **Scope:** only the driving-behaviour chapters (Ch 2 Safe and Responsible Driving + Ch 3 Signs and Lights)? Leave out licensing, insurance and snowmobiles for now?
