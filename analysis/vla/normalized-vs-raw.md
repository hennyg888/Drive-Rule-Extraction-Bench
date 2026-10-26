# Normalized rules vs the raw handbook, for RAG and a VLA

michael's question (11 Oct): what does the normalized rule translation change, compared with giving RAG or a VLA the raw handbook? Is the VLA better at understanding it, is RAG easier, is grounding better, or what else does the normalized form offer?

## Short answer

Readability is not the main advantage. LLMs read the handbook's prose well, and raw-text RAG already works on simple cases: DriveReg went from 76% to 100% decision accuracy on its 76 hypothetical scenario–action pairs by retrieving regulation text. Normalization doesn't save space either. The 93 handbook text passages and our 88 statements are each about 12k characters, roughly 3k tokens.

What changes is **who settles each question, and when**. With the raw handbook, the model has to settle these questions itself, quietly, at every decision:

- which sentences make one rule;
- when the rule applies;
- whether it is law or advice;
- what overrides it;
- which words are vague.

Normalization settles them once, writes the answer into the statement, and lets a person check it. The gains follow from that.

| | Raw handbook | Normalized rules | Gain |
|---|---|---|---|
| **RAG** | A sentence can lose its condition, and a paragraph bundles several rules | One rule per item, self-contained, typed and tagged | Clear: right-sized retrieval units and exact keys |
| **VLA reasoning** | The model infers strength, conditions, exceptions and references | Stated in the rule | Likely, untested: removes the steps LLMs get wrong most often |
| **Grounding** | Many sentences have no explicit condition to ground | Explicit conditions, one phrase per concept | Large: the grounding layer needs this anyway |
| **Tracing and checking** | A citation is a sentence only a person can judge | A citation names a condition and a strength that can be compared with the scene and the action | Large |

## What our 88 statements show

Each count compares the statements in `passing-rules/mto/rules.json` with the handbook passages they came from (michael's 96 passages plus the census sentences).

1. **The deciding condition sits outside the sentence.** For 17 of the 75 rules and exceptions, a condition that decides when the rule applies never appears in its own handbook sentences. In 15 it is in the heading, and in 2 it is in a neighbouring sentence. (Corrected on 20 October from 16 and 14: 3.5.2a takes its towing scope only from the Towing page.) Examples:
   - "Be patient. Avoid passing, changing lanes and crossing traffic." applies only in fog or blowing snow, and says so only in the heading.
   - "Stay well back and do not pass until it is safe to do so." is about farm machinery.
   - "Whenever possible, you should change lanes to pass." is about cyclists.
   - "Do not pass on this road." is the meaning of a sign.

   A retriever indexing sentences can't connect the first one to fog. A model that receives it with no heading reads it as a general rule.
2. **Some sentences mean nothing on their own.** "(See Diagram 2-11.) Failure to do so may result in a fine and an additional two demerit points" never mentions cyclists or 1 m. Other examples are "However, they can use any part of the lane…" (they are cyclists) and "These left-turn lanes…". 3.4.4b puts the duty and its penalty in one statement.
3. **Rules and passages don't line up one to one.**
   - 16 of the 88 passages that statements draw on feed 2 or 3 statements. For example, m51 feeds 3.4.2a, 3.4.2b and 3.4.2c.
   - 14 statements combine 2 to 5 passages. The two passing procedures alone take 5 and 4.
   - Paragraph chunks avoid lost context, but then hand the model several rules at once to split up.
4. **Law or advice is usually not stated in the sentence.** For 51 of the 73 rules, the sentence carries no word that decides the strength:
   - 42 are bare imperatives;
   - 3 are cautions;
   - 3 take their strength from a section heading;
   - 3 rest on a default reading or an implication.

   All three heading cases are legal rules. "Do not pass on this road" is a regulatory sign, and that section says such signs "must be obeyed". "Driving to prevent another vehicle from passing" is listed under sanctions. Reading the sentence alone, a model has to guess. The rule language decides once and records the reason in STRENGTH FROM.
5. **Exceptions and variants live in other passages.** Three of the five links between statements join different passages:
   - the school-bus median exception (c4) and the rule it changes (c1, c5);
   - passing at night and the general passing steps;
   - not cutting in and those same steps.

   A retriever that returns one passage won't return the other. The link in the statement brings it along.
6. **The wording drifts.** "Pass" also means "go past" in sentences that aren't about overtaking, such as "Wait for the emergency vehicle to pass" and "slow down and pass carefully" (animals). Five of michael's passages (m92 to m96) use the word that way or concern someone else passing, and none of them became a passing rule. "Overtake" appears 6 times for the same manoeuvre, and "you" or "your" 103 times. The rule language uses one phrase per concept and names the role.
7. **Vague words aren't marked.** In the handbook they look like any other word. The rules mark 50 vague spans inline, and 53 statements carry a flag.

## What that means for each part

- **RAG.** A normalized statement is what Dense X Retrieval calls a proposition: an atomic, self-contained unit. Indexing a corpus by propositions retrieved better than indexing by passages, and helped downstream QA at the same compute budget. That evidence comes from open-domain QA, not driving. Here, the normalized form also allows two things raw text can't do without first doing the same annotation work:
  - filtering by type (law, advice, fact);
  - exact keys (tags and conditions), with links that bring exceptions along.
- **VLA reasoning.** Four steps disappear: inferring strength, attaching conditions from headings, finding exceptions, and resolving "they", "these" and "do so". These are the steps where LLMs have been seen to fail most.
  - RuleArena found that LLMs struggle to identify and apply the right rule and get confused by similar ones.
  - Zin et al. (in the Paper folder) found that turning traffic rules into Logical English needs context the original leaves out, and that LLMs often fail to supply it correctly.

  The marked vague spans also tell the model where its own judgment is expected and must be explained.
- **Grounding.** "Be patient. Avoid passing, changing lanes and crossing traffic." has no condition to ground. "a driver SHOULD NOT pass WHEN driving in fog" has exactly one: `weather = fog`. With one phrase per concept, each condition maps to one predicate. The grounding layer in `rules-for-vla.md` can only be built on normalized rules; starting from raw text, you would end up normalizing anyway.
- **Tracing and checking.** A VLA that cites 3.3.2a commits to a condition (fog) and a modal (SHOULD NOT). A checker can compare both with the scene and the action. A VLA that cites a handbook sentence leaves the check to a person. Every statement keeps its source sentence, so the trace still ends in the handbook.

## Costs and risks

- **Normalization can be wrong**, for example a strength decision or a dropped nuance. The model will inherit the error. Attached sources, the census and the flags make errors reviewable, but they don't prevent them.
- **Some meaning moves out of the rule.** Examples and reasons go into BECAUSE or FACT statements. Give the VLA the FACT statements too, or it loses some of the "why".
- **It is work.** The full handbook is 3,444 sentences.
- **A hedge:** give the VLA a card with the normalized rule and its source sentence together, at least while testing.

## Shown so far, and not yet

- **Shown:** the structural differences above, counted on our own data.
- **Not shown: that they make a VLA decide better.** I expect they do, but it is untested. Comparison A1 vs A2 in `rules-for-vla.md` §5 tests it. Build its test set mainly from the cases above, where raw text is weakest:
  - the 17 conditions held in headings or neighbouring sentences;
  - the 3 legal rules whose strength comes from a heading;
  - the 3 cross-passage links;
  - the split rule and penalty.

  Add matched simple cases, where both forms should do equally well.
- **Retrieval can be tested first, with no VLA.** Index the same content three ways: raw sentences, raw paragraphs with their headings, and normalized statements. For each test scene, measure how many of the applicable rules come back, and how many inapplicable ones come with them.

## Sources

- Chen et al., *Dense X Retrieval: What Retrieval Granularity Should We Use?*, EMNLP 2024. [arXiv 2312.06648](https://arxiv.org/abs/2312.06648)
- Choi et al., *Decontextualization: Making Sentences Stand-Alone*, TACL 2021. [ACL Anthology](https://aclanthology.org/2021.tacl-1.27)
- Zhou et al., *RuleArena: A Benchmark for Rule-Guided Reasoning with LLMs in Real-World Scenarios*, ACL 2025. [arXiv 2412.08972](https://arxiv.org/abs/2412.08972)
- Cai et al., *Driving with Regulation* (DriveReg). [arXiv 2410.04759](https://arxiv.org/abs/2410.04759)
- Zin et al., *Towards Machine-Readable Traffic Laws: Formalizing Traffic Rules into PROLOG Using LLMs*, in the Paper folder.
