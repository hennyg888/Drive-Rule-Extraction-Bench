# Prior-work search prompt (10 October 2026)

Before the template plan (`analysis/rule-template-plan.md`) was written, a Claude subagent searched for prior designs with the prompt below, from 21:58 to 22:02 UTC on 10 October 2026. Its report fed §5 of the plan. The prompt is copied verbatim.

```
Research task (do NOT call any mcp__hearthbot__ tools; just return a report to me). Do not install packages.

Context: a lab project converts the Ontario MTO Driver's Handbook into "formal rules" written in a natural-language-like controlled template language (not LTL/symbolic), designed as a MINIMAL set of fixed keywords/patterns (like SQL's small keyword set) so an LLM/VLM can reason over them. Content types seen in the handbook: obligations/prohibitions (must, must not, illegal), permissions (may, only if), advisory (should, avoid, never as advice), cautions (watch for, be prepared), procedures (ordered steps with done-conditions and fallbacks), definitions, background facts, exceptions (unless/except), reasons (because), penalties (fines, demerit points), vague/judgment terms (safe, enough, if in doubt, as soon as you can).

Use WebSearch (and WebFetch where useful) to find prior designs we can borrow from. For each, give: name, citation/URL, what its keywords/patterns are (quote the actual pattern set where possible), and what specifically we could borrow or what to avoid. Cover at least:
1. EARS (Easy Approach to Requirements Syntax, Mavin et al.) – its 5-6 patterns.
2. SBVR (OMG Semantics of Business Vocabulary and Rules) Structured English and RuleSpeak – modal keywords (It is obligatory that / permitted / necessary), vocabulary/term definitions.
3. Logical English (Kowalski) and Catala (legal programming language with default/exception logic).
4. Attempto Controlled English (ACE) and other CNLs for rules; Gherkin Given/When/Then briefly.
5. LegalRuleML / deontic modelling of obligations, permissions, prohibitions, defeasibility.
6. Traffic-rule formalization work: Rulebooks (Censi et al. 2019, rule hierarchy/priorities), Rizaldi et al. Isabelle formalization of traffic rules for overtaking (German StVO / Vienna Convention), Maierhofer et al. formalization of interstate traffic rules (overtaking), any work on traffic rules in Metric Temporal Logic, and recent (2023-2026) LLM-based traffic rule extraction/formalization or LLM driving with traffic-rule knowledge retrieval (e.g. papers that convert driving handbooks/regulations into structured rules with LLMs; "driving with regulation", "LLM traffic rules", "LeGEND", etc.). Note how they handle vague terms (e.g. "safe distance") and exceptions.
7. Any work on handling vagueness/open-texture in legal rule formalization (e.g. marking judgment predicates, "open texture").

Keep the report under ~1500 words, structured, with URLs. Clearly mark anything you couldn't verify.
```
