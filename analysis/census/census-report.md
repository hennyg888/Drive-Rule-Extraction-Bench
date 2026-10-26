# Handbook census

Written on 10 October 2026, while the rule language was being designed: "v0" is its first draft and "v1" the version this census led to, and the field now called strength (`STRENGTH FROM`) was then called force (`FORCE FROM`). The current language is `analysis/rule-language.md`; git keeps the earlier versions.

Every sentence of the MTO Driver's Handbook was labelled against rule language v0 to decide what v1 needs. 3,444 sentences were labelled (paragraphs split into sentences, plus list items, numbered steps and captions; headings and the sample test page were left out, the test page because it is kept for evaluation). The labels are LLM output following `census-guidelines.md`; they have not been checked by a person, so the counts are evidence for design choices, not ground truth.

Files: `census-labels.jsonl` (one line per sentence: id, page, section, text, labels), `census-guidelines.md` (the labelling instructions), `census-summary.json` (all counts below).

## 1. What the handbook is made of

| Type | Sentences | Share |
|---|---|---|
| Rule (instruction, permission, advice, caution) | 1,683 | 48.9% |
| Fact (no instruction) | 789 | 22.9% |
| Navigation, headings in running text, references | 361 | 10.5% |
| Penalty or other consequence | 201 | 5.8% |
| Step of a procedure | 310 | 9.0% |
| Definition | 100 | 2.9% |


Rules and steps together: 1,993 sentences (57.9%). Those are the "normative" sentences the shares below refer to.

## 2. Legal force

| Modal | Rules and steps | Share |
|---|---|---|
| MUST | 287 | 14.4% |
| MUST NOT | 110 | 5.5% |
| MAY | 216 | 10.8% |
| SHOULD | 1,186 | 59.5% |
| SHOULD NOT | 190 | 9.5% |


Where the force came from:

| Basis | Rules and steps | Share |
|---|---|---|
| Bare imperative (defaults to SHOULD) | 1,185 | 59.5% |
| Legal wording | 390 | 19.6% |
| Permission wording | 185 | 9.3% |
| Advice wording | 184 | 9.2% |
| None | 49 | 2.5% |


153 rules are cautions (written `SHOULD WATCH FOR`). 239 sentences carry an `M` flag (unclear legal force), about 12.0% of the normative ones. Most are bare imperatives on the rules-of-the-road pages where a law sits behind the advice ("Come to a complete stop", "Keep to the right-hand road"), and "must" used as encouragement in the safe-driving chapter. This is the hardest part of the language to get right, which is why v1 records `FORCE FROM` on every rule.

## 3. Clauses

| Clause meaning found in the sentence | Rules and steps | Share |
|---|---|---|
| WHEN (situation or event) | 1,070 | 53.7% |
| purpose ("to", "so that") | 257 | 12.9% |
| before / after (source wording) | 209 | 10.5% |
| number or threshold | 203 | 10.2% |
| WHILE (ongoing state) | 153 | 7.7% |
| ONLY IF | 96 | 4.8% |
| if … then (source wording) | 91 | 4.6% |
| exception to another passage | 68 | 3.4% |
| BECAUSE (reason) | 66 | 3.3% |
| until (no v0 keyword) | 58 | 2.9% |
| UNLESS | 46 | 2.3% |
| hedged default | 21 | 1.1% |
| IF VIOLATED, inline | 1 | 0.1% |


These count what the sentence means, not which keyword the rewrite used. "if … then" and "before / after" sentences were nearly all rewritten with `WHEN`, `ONLY IF` or step order at full fit.

## 4. How much v0 could express

| Type | Sentences | Full fit | Share | Partial | None |
|---|---|---|---|---|---|
| RULE | 1,683 | 1,530 | 90.9% | 153 | 0 |
| STEP | 310 | 306 | 98.7% | 4 | 0 |
| DEFINE | 100 | 74 | 74.0% | 26 | 0 |
| CONSEQ | 201 | 158 | 78.6% | 43 | 0 |


Across all rewritten sentences, 90.1% fit v0 fully and none failed outright. What the partial ones needed:

| Need | Sentences | Example |
|---|---|---|
| list lead or definition by list | 65 | “As of May 11, 2026, when you apply for your class G or class M licence, you will need to declare that:” |
| right-of-way relation | 44 | “In most cases, that means yielding to the pedestrian.” |
| UNTIL | 40 | “After six months with your G2 licence and until you obtain your full G licence or turn 20, you are allowed to …” |
| time window | 17 | “Until 2011, all individuals will need to be re-certified before renewing their permit.” |
| BEFORE/AFTER | 10 | “Give the correct signal well before taking the action and make sure other drivers can see it.” |
| question form (self-test) | 10 | “Am I experiencing an increasing number of near collisions?” |
| cumulative threshold (points over a period) | 10 | “If you accumulate too many demerit points, your driver’s licence can be suspended.” |
| rule by reference (role inheritance, deeming, scope) | 9 | “A pickup truck towing a house trailer exceeds 4,600 kilograms, but the total combined weight of the truck and …” |
| consequence without a broken rule | 8 | “If you cancel or reschedule your road test appointment with less than 48 hours notice, or if you fail to atten…” |
| hedged modality (may need, may or must) | 6 | “A sign with a green circle means you may or must do the activity shown inside the ring.” |
| duty or liability of another role | 6 | “Drivers on both roads are equally responsible for seeing that traffic merges smoothly and safely.” |
| requirement on a thing (no role) | 5 | “Child car seats must meet Canadian Motor Vehicle Safety Standards.” |
| generic default (generally, most) | 5 | “Most buses and other public vehicles are required to stop at railway crossings that are not protected by gates…” |
| emphasis (especially) | 4 | “This is especially true when driving around large commercial vehicles, as they typically have large blind spot…” |


## 5. Decisions for v1

| Decision | What | Why |
|---|---|---|
| Added | UNTIL | UNTIL. 58 instructions say a duty lasts until something happens (stop until the bus moves, wait until the fog lifts), and v0 could not write 37 of them. Writing them as WHILE NOT turns the handbook's wording inside out, and several are safety rules. |
| Added | FORCE FROM (metadata) | FORCE FROM on every rule. 239 sentences, about 12% of the instructions, have unclear legal force, mostly bare imperatives with a law behind them. Recording whether the force came from the wording, the imperative default or the section context lets them be raised later without guessing now. |
| Added | SEE (metadata) | SEE as metadata. The handbook has 245 images and diagrams; a diagram goes with a rule but never changes when it applies, so SEE names the figure instead of being a clause. |
| Kept | All v0 clauses and modals | Every v0 clause is in use: WHEN in 1,070 instructions, WHILE in 153, ONLY IF in 96, UNLESS in 46, exceptions across passages in 74, penalties in 201 sentences. |
| Kept | Imperatives default to SHOULD | Bare imperatives stay SHOULD by default. They are the most common kind of instruction (1,185, 59%); section context or an offence table can still make one law, with the reason recorded. |
| Kept | SHOULD WATCH FOR | Cautions stay SHOULD WATCH FOR. All 153 cautions fit it without a separate keyword. |
| Not added | BEFORE / AFTER | BEFORE / AFTER. 209 instructions mention order, and 174 of them were written at full fit with step order, WHEN about to …, or ONLY IF the driver has first …; only 10 asked for a keyword. |
| Not added | IF … THEN in rules | IF … THEN outside procedures. 45 rules are worded "if … then" in the handbook, and 37 were written with WHEN at full fit, so IF … THEN stays a procedure branch. |
| Not added | SO THAT (purpose) | SO THAT. 257 instructions give a purpose; 248 were written at full fit with BECAUSE this … or a plain "to …", so purpose shares BECAUSE. |
| Not added | Quantities, lists, right of way | Quantities, lists and right of way are wording, not keywords. 203 instructions carry a number and fixed phrases cover them ("at least", "within 30 m of"); 65 partial fits came from list leads ("Bring the following:"), handled as one statement per item; 44 needed "yield the right-of-way to", which is a verb phrase. |


## 6. Vague content

| Code | Meaning | Flags | Most frequent wording |
|---|---|---|---|
| J | Judgment term | 632 | "the way is clear" (15), "safely" (13), "too closely" (9), "enough space" (8), "carefully" (7), "with caution" (7) |
| M | Unclear legal force | 239 | "stop at the edge of the sidewalk" (7), "stop at the edge of the intersection" (7), "you may have to accelerate more quickly" (6), "stop at the crosswalk" (5), "bring the following items to the test" (3), "money for test fees" (3) |
| S | Hedged scope | 171 | "often" (19), "usually" (13), "generally" (9), "typically" (4), "some roads" (3), "some drugs" (3) |
| R | Unclear reference or role | 119 | "this" (8), "these entrances" (5), "it" (4), "these demands" (4), "certain conditions" (3), "any of these demands" (3) |
| D | Implicit default | 33 | "where permitted" (2), "if you fail or refuse to provide a breath sample" (2), "you have 60 days to continue to use your existing driver’s licence" (1), "driving while your licence is suspended" (1), "bike lanes are reserved for cyclists" (1), "sometimes you will need to enter or cross a bike lane" (1) |
| G | Goal and means differ | 4 | "passing left of a centreline" (1), "slow down and pass carefully" (1), "don't try to drive around the animal" (1), "speed up to pass a vehicle moving slowly" (1) |


1,048 sentences (30.4%) have at least one flag. `V` (wording drift) and `X` (stated twice) need two passages side by side, so they were only flagged in the passing rules, not in the census.

## 7. By chapter

| Ch. | Title | Sentences | Rules+steps | Facts | Defs | Conseq. | Legal wording | Bare imperative | Full fit | Passing |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | The Official Ministry of Transportation (MTO) Driver’s Handbook | 21 | 3 | 8 | 0 | 0 | 0 | 2 | 100.0% | 0 |
| 1 | Getting Your Driver’s Licence | 321 | 200 | 49 | 7 | 5 | 74 | 52 | 89.6% | 3 |
| 2 | Safe and Responsible Driving | 1,449 | 931 | 319 | 53 | 22 | 115 | 639 | 90.1% | 145 |
| 3 | Traffic Signs and Lights | 313 | 143 | 133 | 12 | 2 | 50 | 59 | 86.0% | 13 |
| 4 | Keeping Your Driver’s Licence | 304 | 75 | 67 | 10 | 124 | 29 | 15 | 80.9% | 5 |
| 5 | Your Vehicle | 208 | 135 | 42 | 6 | 2 | 34 | 76 | 91.6% | 12 |
| 6 | The Level Two Road Test | 353 | 257 | 62 | 3 | 1 | 5 | 218 | 98.9% | 10 |
| 7 | Off-road Vehicles & Snowmobiles | 475 | 249 | 109 | 9 | 45 | 83 | 124 | 91.1% | 0 |


## 8. Passing content outside the 96 passages

188 sentences were labelled as being about passing. Matching them against the 96 passages on the Passing Topic Comparison page leaves these:


**Missing from the passing set, now added to the rules** (8)

- Stopping › Stopping for school buses: “You must stop whenever you approach a stopped school bus with its upper alternating red lights flashing, regardless of whether you are behind the bus or approaching it from the front.” The rule behind 3.4.12a: passing a school bus with its red lights flashing is illegal because every driver must stop. The handbook states this law on three pages. Now rule 3.4.12b.
- Stopping › Stopping for school buses: “If you are coming from behind the bus, stop at least 20 metres away.” Now rule 3.4.12c.
- Stopping › Stopping for school buses: “Do not go until the bus moves or the lights have stopped flashing.” Written with UNTIL in v1. Now rule 3.4.12d.
- Stopping › Stopping for school buses: “If you are on a road with a median strip, only vehicles coming from behind the bus must stop.” Now rule 3.4.12e.
- Stopping › Stopping for school buses: “If you don't stop, you can be fined heavily and get six demerit points for a first offence.” Its penalty. Now rule 3.4.12b.
- Changing directions › Left turns: “If you are making a left turn behind one of these vehicles, do not pull up beside it to make your turn at the same time.” Same paragraph as 3.4.3a. Pulling up beside a turning motorcycle or bicycle is the start of a pass. Now rule 3.4.3b.
- Changing directions › Left turns: “Stay behind and turn when the way is clear.” The positive form of the same rule. Now rule 3.4.3c.
- Signs › Regulatory signs > Here are some common regulatory signs:: “Slow traffic on multi-lane roads must keep right.” A regulatory sign whose caption itself says "must". It is the legal side of keeping right for faster traffic (2.1d, 3.6.1a). Now rule 3.6.1d.

**Related, left for you to decide** (26)

- Driving along › Keep right: “This is especially important if you are driving more slowly than other vehicles.” The sentence after 2.1d's source; it ties keeping right to being passed.
- Sharing the road with other road users › Sharing the road with pedestrians: “Pass these safety islands and zones at a reasonable speed.” Repeats 3.4.5d on the pedestrians page (now flagged X).
- Sharing the road with other road users › Sharing the road with pedestrians: “Always be ready, in case pedestrians make sudden or unexpected moves.”
- Sharing the road with other road users › Sharing the road with cyclists: “Bicycles and mopeds travelling at a lower speed than other traffic are expected to ride about one metre from the curb or parked cars, or as close as practical to the right-hand edge of the road when there is no curb.” Where a cyclist rides, which sets the room needed to pass (3.4.4).
- Sharing the road with other road users › Sharing the road with cyclists: “Cyclists are not required to ride close to the right edge of the road when they are travelling at or faster than the normal speed of traffic at that time and place, or when they are turning left, or getting in position to turn left.”
- Sharing the road with other road users › Sharing the road with large commercial vehicles: “If a large vehicle in front of you is making a right turn, do not move up into the space that opens up in the right lane; you are putting yourself into a very dangerous position.” Moving up beside a large vehicle while it turns; close to passing it on the inside.
- Sharing the road with other road users › Sharing the road with large commercial vehicles: “Stay well back until the truck has completely cleared the lane.”
- Sharing the road with other road users › Sharing the road with large commercial vehicles: “Do not drive up into the left lane when a large vehicle is making a left turn in front of you.”
- Sharing the road with other road users › Sharing the road with large commercial vehicles: “Stay well back until the truck has cleared the left turn, or else you may get squeezed between the truck and the curb.”
- Sharing the road with other road users › Sharing the road with school buses: “When you see a school bus with its overhead amber lights flashing:” Amber lights: slow down and prepare to stop.
- Sharing the road with other road users › Sharing the road with school buses: “Slow down and prepare to stop whether you are behind or approaching the bus”
- Sharing the road with other road users › Sharing the road with school buses: “You must stop whether you are behind or approaching the bus” Sharing the road repeats the school bus law (076.1 to 081.1).
- Changing directions › Dealing with particular situations at a roundabout > Pull over for emergency vehicles: “If you have not entered the roundabout yet, pull over to the right if possible and wait until the emergency vehicle has passed.”
- Changing positions › Changing lanes: “Remember that spending a few seconds behind another vehicle is often safer than going around it.” In the Changing lanes section you left out, but it is advice about passing.
- Dealing with particular situations › Workers on the road: “If safe to do so, move over a lane to increase the space between your vehicle and the hazard.” Same paragraph as the workers-on-the-road passage you left out.
- Dealing with particular situations › Reacting to an approaching emergency vehicle: “When the emergency vehicle has passed, check to make sure the way is clear and signal before merging back into traffic.” Being passed by an approaching emergency vehicle, which has its own procedure.
- Dealing with particular situations › Reacting to a stopped emergency vehicle or tow truck: “When safe to do so, change lanes well in advance of an emergency vehicle or a stopped tow truck with its flashing amber lights.” Repeats 3.4.13b as a step.
- Dealing with particular situations › Reacting to a stopped emergency vehicle or tow truck > Failing to respond to an emergency vehicle: “Please note the above law, fines and penalties are also applicable to a tow truck with its lamp producing intermittent flashes of amber light that is stopped on a highway.” Extends 3.4.13 to tow trucks, which the rules already include.
- Signs › Regulatory signs > Here are some common regulatory signs:: “Stop for school bus when signals are flashing.” The school bus sign on the Signs page.
- Keeping Your Driver’s Licence › Table of offences > Six points: “Failing to stop for a school bus” The offence table: 6 demerit points.
- Keeping Your Driver’s Licence › Table of offences > Two points: “Failing to share the road” Possibly the offence behind 3.6.1a and the 1 m rule (3.4.4b); the handbook does not connect them.
- The Level Two Road Test › Left and right turns > If stopped > Space: “When stopped behind another vehicle at an intersection, leave enough space to pull out and pass without having to back up.” Road-test advice to leave room to pull around the vehicle ahead; said three more times in that chapter.
- The Level Two Road Test › Left and right turns > If stopped > Wheels: “At a large intersection with curved sidewalks where you are turning right, angle your vehicle to follow the curb so that no other vehi­cle can fit between you and the curb.” Leaving no gap on the right while turning, so no one passes there.
- The Level Two Road Test › Left and right turns > Making the turn > Traffic check: “If it is possible for another vehicle to overtake you while you are turning, check your blind spot before starting to turn.” Being passed while turning.
- The Level Two Road Test › Through intersection > Driving through > Lane: “If your lane is blocked by a vehicle turning left or a vehicle edging into the intersection from the right, slow down or stop instead of pulling out to go around the vehicle.” Not pulling out to go around a vehicle that blocks the lane.
- The Level Two Road Test › Roadside stop > The approach > Traffic check: “If there is a chance of traffic or pedestrians overtaking you on the right, check your right blind spot just before pulling over.” Being passed on the right while pulling over.

32 more were headings, test-topic lists or only loosely about passing; they are in `census-labels.jsonl` with `"pass": true`.


## 9. Limits

- One labeller per sentence and no second opinion, so there is no agreement score. A useful next check is to label a random 100 sentences twice and compare `t`, `m` and `fit`.
- The sentence splitter keeps list items and steps as their own units, so a list lead ("Bring the following:") and its items are labelled apart; that inflates the list/enumeration need.
- `fit` was judged by the labeller against v0. A FULL fit means the rewrite was possible, not that it is the rewrite we would choose.
