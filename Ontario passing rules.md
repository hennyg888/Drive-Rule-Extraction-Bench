# Ontario passing rules

Oct 14, 2026 · @Henry

66 formal rules about passing, taken from the Official MTO Driver's Handbook. Every rule uses one grammar and a fixed vocabulary, and cites the handbook section, page and any diagram it comes from. The exact quotes are in Source quotes.

Page numbers are the PDF pages of the uploaded handbook (footer "n/221", printed 2026-09-29). The handbook says it is only a guide; for official purposes it points to the Highway Traffic Act.

## Rule format

Every rule is one sentence in this grammar. Words in CAPITALS are keywords or defined terms.

```
RULE      := "WHEN" CONDITION "," "the" ACTOR MODAL ACTION ["," "UNLESS" EXCEPTION] "."
CONDITION := FACT { ("AND" | "OR") FACT }
ACTOR     := PASSER | PASSED DRIVER | DRIVER | CYCLIST   (optionally qualified, e.g. "DRIVER of a large truck")
MODAL     := MUST | MUST NOT | SHOULD | SHOULD NOT | MAY | MAY ONLY
ACTION    := what the ACTOR does, or must not do
EXCEPTION := FACT { ("AND" | "OR") FACT }
```

Each rule also carries these fields:

| Field | Content |
| --- | --- |
| ID | PASS-\<GROUP>-\<NN>, for example PASS-LOC-01. Groups: GEN, PROC, LOC, MARK, SIDE, LANE, NIGHT, USER, SC, STOP, BEING, TOW |
| Title | A short name for the rule |
| Force | How strongly the handbook words it: REQUIREMENT, INSTRUCTION, ADVICE or PERMISSION (see Keywords) |
| Penalty | Only when the handbook states one, with its page |
| Note | Anything inferred, combined from two places, or worded ambiguously in the handbook |
| Source | Chapter › section › subsection, p. N; Diagram X-Y. The exact words are in the Source quotes tab |

Citation style: chapter and section names are the handbook's own headings. “p. N” is the PDF page. A diagram is cited by its handbook number, and its content is described in the Source quotes tab. A rule that rests on a diagram alone says so in its Note (PASS-PROC-08).

A machine-readable copy of the same rules (YAML, same IDs and fields) was delivered alongside this doc.

## Keywords

The Force of a rule records how the handbook words it. The Force then fixes which MODAL the rule may use.

| Force | Handbook wording that triggers it | Allowed MODAL |
| --- | --- | --- |
| REQUIREMENT | “must”, “required”, “not permitted”, “may not”, “not allowed”, “unlawful”, “illegal”; a regulatory-sign direction; or a stated penalty | MUST, MUST NOT |
| INSTRUCTION | A plain command: “do”, “don't”, “never”, “use”, “watch”, “stay” | MUST, MUST NOT |
| ADVICE | Softer wording: “should”, “avoid”, “be careful”, “unsafe”, or a description of normal practice | SHOULD, SHOULD NOT |
| PERMISSION | “may”, “you can” | MAY, MAY ONLY |

| MODAL | Meaning |
| --- | --- |
| MUST | The ACTION is required whenever the CONDITION holds |
| MUST NOT | The ACTION is prohibited whenever the CONDITION holds |
| SHOULD / SHOULD NOT | Recommended or discouraged; departing from it is not called unlawful by the handbook |
| MAY | The ACTION is allowed when the CONDITION holds |
| MAY ONLY | Allowed when the CONDITION holds, and prohibited otherwise |
| AND / OR / UNLESS | Logical connectors inside CONDITION and EXCEPTION |

When two passages word the same rule differently, the stronger wording is recorded and the Note says so. Force reflects the handbook's wording only. Whether something is an offence is decided by the Highway Traffic Act.

## Vocabulary

These terms keep one meaning in every rule. They are written in CAPITALS where they are used.

| Term | Meaning in this rule set | Basis in handbook |
| --- | --- | --- |
| PASS | The manoeuvre of changing lanes to move past a slower vehicle travelling in the same direction, then returning to the ORIGINAL LANE. Used interchangeably with ‘overtake’. | p. 67: “Passing is changing lanes to move past a slower vehicle.” |
| PASSER | The driver making a PASS. Unless a rule says otherwise, this is the ACTOR. | Defined for this rule set |
| PASSED VEHICLE / PASSED DRIVER | The vehicle, and its driver, being overtaken. | Defined for this rule set |
| DRIVER | Any driver, whether passing or not. | Defined for this rule set |
| ORIGINAL LANE | The lane the PASSER was in before the PASS began. | p. 68: “Go back to your original lane.” |
| PASSING LANE | In the steps for a PASS: the lane the PASSER moves into. As a road feature: an extra lane provided so faster traffic can pass (see CLIMBING LANE). | pp. 67, 70 |
| CLIMBING LANE | An extra right-hand lane, often on grades, that lets slower vehicles move right so faster ones can pass in the left lane. | p. 70, Diagram 2-48 |
| TRUCK PASSING LANE | On roads with three or more lanes each way where trucks are barred from the far-left lane: the lane next to it. | p. 69 |
| CENTRE LINE | The marking separating opposing traffic. Yellow lines separate opposing traffic; white lines separate traffic in the same direction. | p. 137 |
| SOLID LINE / BROKEN LINE | A continuous or dashed pavement line at the left of the PASSER's lane. | p. 137, Diagrams 3-1, 3-2 |
| MULTI-LANE ROAD | A road with two or more lanes in the same direction. | p. 66 |
| ONE-WAY ROAD | A road on which all traffic travels in one direction. | p. 70 |
| SHOULDER | The strip beside the travelled lanes, paved or unpaved. | p. 70 |
| ONCOMING TRAFFIC | Traffic approaching in the opposite direction. | p. 68 |
| CLEAR DISTANCE | Unobstructed road ahead that is long enough to complete a PASS safely. | p. 68 |
| ALONGSIDE | The phase of a PASS when the PASSER is level with the PASSED VEHICLE. | p. 69 |
| BLIND SPOT | Area around the vehicle not visible in the mirrors; checked by looking over the shoulder. | p. 66 |
| PEDESTRIAN CROSSOVER | A designated crossing without traffic lights, marked by signs, overhead yellow lights, and double white lines with an X in each lane. | pp. 55, 139 |
| CROSSWALK | The part of a roadway linking sidewalks, or marked by signs or lines for pedestrian crossing, marked or not. | p. 37 |
| CYCLIST | A person riding a bicycle. | pp. 39–40 |
| LARGE VEHICLE | A large commercial vehicle, such as a truck, tractor-trailer or bus. | pp. 42–44 |
| LCV | Long commercial vehicle: a double trailer up to 40 metres long, identified by a rear placard. | p. 128 |
| SLOW-MOVING VEHICLE SIGN | An orange triangle with a red border meaning the vehicle travels at 40 km/h or less. | pp. 45, 128 |
| EMERGENCY VEHICLE | A police, fire, ambulance or public-utility emergency vehicle using red or blue flashing lights, siren, bell, or alternating white high beams. | p. 88 |
| SCHOOL BUS | A chrome-yellow bus marked ‘School Bus’. | p. 53 |
| MEDIAN | A physical barrier (raised, lowered, earth or paved strip) separating opposing traffic that vehicles cannot cross. | p. 54 |
| STREETCAR | A rail transit vehicle running on the road. | pp. 70–71 |
| FREEWAY | A high-speed, controlled-access highway. | pp. 77–80 |

## GEN — General conditions

| ID | Rule | Force | Source |
| --- | --- | --- | --- |
| PASS-GEN-01 | **Pass only when it is safe.** WHEN any PASS is contemplated, the PASSER **MUST NOT** begin the PASS, UNLESS the PASSER is sure the PASS can be completed without danger to the PASSER or others. | INSTRUCTION | Safe and Responsible Driving › Changing positions › Passing, p. 67 |
| PASS-GEN-02 | **If in doubt, do not pass.** WHEN the PASSER is in doubt about whether a PASS is safe, the PASSER **MUST NOT** begin the PASS. | INSTRUCTION | Safe and Responsible Driving › Changing positions › Passing, p. 67 |
| PASS-GEN-03 | **Space and time to complete.** WHEN about to begin a PASS, the PASSER **MUST** confirm there is enough space and time to complete the PASS safely. | INSTRUCTION | Safe and Responsible Driving › Changing positions, p. 66 |
| PASS-GEN-04 | **Keep right except to pass.** WHEN driving on any road, the DRIVER **MUST** keep to the right of the road, or in the right-hand lane of a MULTI-LANE ROAD, UNLESS the DRIVER is turning left or making a PASS. *Note:* The handbook adds that this is especially important when driving more slowly than other vehicles. | INSTRUCTION | Safe and Responsible Driving › Driving along › Keep right, p. 34 |

## PROC — Passing procedure

| ID | Rule | Force | Source |
| --- | --- | --- | --- |
| PASS-PROC-01 | **Signal left and check before moving out.** WHEN preparing to move into the PASSING LANE, the PASSER **MUST** activate the left-turn signal AND check that the way is clear ahead and behind. | INSTRUCTION | Safe and Responsible Driving › Changing positions › Passing › steps for passing, step 1, p. 67 |
| PASS-PROC-02 | **Lane-change checks apply to a pass.** WHEN moving out of, or back into, the ORIGINAL LANE (a PASS begins and ends with a lane change), the PASSER **MUST** check mirrors for a safe gap, check the BLIND SPOT over the shoulder, signal, check again, then steer gradually into the new lane without slowing down. *Note:* Linking the lane-change steps to passing is an inference from the handbook placing both under ‘Changing positions’ and defining passing as ‘changing lanes’. | INSTRUCTION | Safe and Responsible Driving › Changing positions › Changing lanes, p. 66; Diagram 2-45 (p. 67); Safe and Responsible Driving › Changing positions, p. 66 |
| PASS-PROC-03 | **Watch for hidden and entering road users.** WHEN a PASS is under way, the PASSER **MUST** watch for bicycles and small vehicles hidden in front of the PASSED VEHICLE, vehicles turning left in front, and vehicles or pedestrians entering from another road or driveway. | INSTRUCTION | Safe and Responsible Driving › Changing positions › Passing › steps for passing, step 2, p. 67 |
| PASS-PROC-04 | **Signal before changing lanes.** WHEN making any lane change that is part of a PASS, the PASSER **MUST NOT** change lanes before signalling. | INSTRUCTION | Safe and Responsible Driving › Changing positions › Passing › steps for passing, step 3, p. 67 |
| PASS-PROC-05 | **Return-to-lane point.** WHEN the PASSER has overtaken the PASSED VEHICLE, the PASSER **MUST** signal the move back AND return to the ORIGINAL LANE only once the entire front of the PASSED VEHICLE is visible in the inside (rear-view) mirror. | INSTRUCTION | Safe and Responsible Driving › Changing positions › Passing › steps for passing, step 3, p. 67; Diagram 2-46 (p. 68) |
| PASS-PROC-06 | **Do not cut off the passed vehicle.** WHEN returning to the ORIGINAL LANE, the PASSER **MUST NOT** cut off the PASSED VEHICLE by moving suddenly in front of it. *Note:* Intentionally cutting off another vehicle is listed as aggressive driving. | INSTRUCTION | Safe and Responsible Driving › Changing positions › Passing › steps for passing, step 3, p. 67; Keeping Your Driver's Licence › Other ways to lose your licence › Sanctions – dangerous behaviours, p. 150 |
| PASS-PROC-07 | **Do not race; abort the pass.** WHEN the PASSED VEHICLE speeds up during the PASS, the PASSER **MUST** abandon the PASS AND return to the ORIGINAL LANE rather than race. | INSTRUCTION | Safe and Responsible Driving › Changing positions › Passing › steps for passing, step 4, p. 68 |
| PASS-PROC-08 | **Cancel the signal.** WHEN the lane change back into the ORIGINAL LANE is complete, the PASSER **MUST** make sure the turn signal is off. *Note:* Diagram-only source: this step appears in the Diagram 2-45 labels but not in the numbered lane-change steps. | INSTRUCTION | Diagram 2-45 (p. 67) |

## LOC — Prohibited and restricted situations

| ID | Rule | Force | Source |
| --- | --- | --- | --- |
| PASS-LOC-01 | **Pedestrian crossover: 30 m.** WHEN within 30 metres of a PEDESTRIAN CROSSOVER, the PASSER **MUST NOT** pass any vehicle. | REQUIREMENT | Safe and Responsible Driving › Changing positions › Passing, p. 68; Safe and Responsible Driving › Stopping › Stopping for pedestrian crossovers, p. 55 |
| PASS-LOC-02 | **Bridge, viaduct or tunnel: 30 m.** WHEN within 30 metres of a bridge, viaduct or tunnel, the PASSER **MUST NOT** pass to the left of the CENTRE LINE. | REQUIREMENT | Safe and Responsible Driving › Changing positions › Passing, p. 68 |
| PASS-LOC-03 | **Hills and curves.** WHEN approaching the crest of a hill OR on a curve, where the view of ONCOMING TRAFFIC is obstructed AND there is not enough CLEAR DISTANCE ahead, the PASSER **MUST NOT** attempt a PASS. | INSTRUCTION | Safe and Responsible Driving › Changing positions › Passing, p. 68 |
| PASS-LOC-04 | **Vehicle stopped at a crosswalk.** WHEN a vehicle is stopped at a CROSSWALK, the PASSER **MUST NOT** pass the stopped vehicle. *Note:* Rationale given: a stopped vehicle may be a clue that a pedestrian is crossing. | INSTRUCTION | Safe and Responsible Driving › Sharing the road with other road users › Sharing the road with pedestrians, p. 37 |
| PASS-LOC-05 | **Centre left-turn lanes.** WHEN a shared centre left-turn lane (used by both directions) is present, the PASSER **MUST NOT** use the left-turn lane for passing. | INSTRUCTION | Safe and Responsible Driving › Changing directions › Left-turn lanes, p. 60 |
| PASS-LOC-06 | **Moving snow plows.** WHEN following a moving snow plow (any conditions), the PASSER **MUST NOT** pass the snow plow. | INSTRUCTION | Safe and Responsible Driving › Changing positions › Passing, p. 67 |
| PASS-LOC-07 | **Between staggered snow plows.** WHEN several snow plows are staggered across a freeway, the PASSER **MUST NOT** pass between them. *Note:* Reason given: not enough room, and the ridge of wet snow can throw a vehicle out of control. | INSTRUCTION | Safe and Responsible Driving › Driving at night and in bad weather › Snow plows, p. 99 |
| PASS-LOC-08 | **Fog.** WHEN driving in fog, the PASSER **MUST NOT** pass other vehicles, or speed up to pass a slow-moving vehicle. *Note:* The DO list uses the softer ‘Avoid passing’ (SHOULD NOT); the REMEMBER list states it absolutely, so the stronger form is used. | INSTRUCTION | Safe and Responsible Driving › Driving at night and in bad weather › Fog › Tips for driving safely in fog (DO), p. 93; Safe and Responsible Driving › Driving at night and in bad weather › Fog › DON'T, p. 94; Safe and Responsible Driving › Driving at night and in bad weather › Fog › REMEMBER, p. 94 |
| PASS-LOC-09 | **Blowing snow and whiteouts.** WHEN driving in blowing snow or whiteout conditions, the PASSER **MUST NOT** attempt to pass a slow-moving vehicle. | INSTRUCTION | Safe and Responsible Driving › Driving at night and in bad weather › Snow › Whiteouts › DO, p. 98; Safe and Responsible Driving › Driving at night and in bad weather › Snow › Whiteouts › DON'T, p. 98 |

## MARK — Pavement markings and signs

| ID | Rule | Force | Source |
| --- | --- | --- | --- |
| PASS-MARK-01 | **Solid line at left of lane.** WHEN there is a SOLID LINE at the left of the PASSER's lane, the PASSER **SHOULD NOT** pass. *Note:* The handbook words this as ‘unsafe’ / ‘should not’, so it is recorded as ADVICE, not REQUIREMENT. The Highway Traffic Act, not the handbook, is the authority on whether it is an offence. | ADVICE | Traffic Signs and Lights › Pavement markings, p. 137; Diagram 3-1 (p. 137) |
| PASS-MARK-02 | **Broken line at left of lane.** WHEN there is a BROKEN LINE at the left of the PASSER's lane AND the way is clear AND enough broken line remains ahead to complete the PASS, the PASSER **MAY** pass. | PERMISSION | Traffic Signs and Lights › Pavement markings, p. 137; Diagram 3-2 (p. 137) |
| PASS-MARK-03 | **‘Do not pass’ sign.** WHEN on a road posted with the ‘Do not pass’ regulatory sign (red circle and slash over two cars), the PASSER **MUST NOT** pass. | REQUIREMENT | Traffic Signs and Lights › Signs › Regulatory signs, p. 111; Traffic Signs and Lights › Signs › Regulatory signs, p. 108 |
| PASS-MARK-04 | **Pilot or pace vehicle sign.** WHEN following a pilot vehicle or pace vehicle displaying the ‘do not pass – when flashing’ sign, the PASSER **MUST NOT** pass that vehicle. *Note:* Recorded as REQUIREMENT because it is a sign direction; the sign image reads ‘WHEN FLASHING’. | REQUIREMENT | Traffic Signs and Lights › Signs › Temporary condition signs, p. 124 |
| PASS-MARK-05 | **Hazard marker shows passing side.** WHEN approaching a hazard close to the edge of the road marked by a striped hazard marker, the PASSER **MAY** pass the hazard on the side to which the marker's stripes slope down. | PERMISSION | Traffic Signs and Lights › Signs › Warning signs, p. 118 |

## SIDE — Which side: left, right and shoulder

| ID | Rule | Force | Source |
| --- | --- | --- | --- |
| PASS-SIDE-01 | **Pass on the left by default.** WHEN making any PASS, the PASSER **SHOULD** pass on the left of the PASSED VEHICLE, UNLESS a case in PASS-SIDE-02 or PASS-SIDE-04 applies. | ADVICE | Safe and Responsible Driving › Changing positions › Passing on the right, p. 70 |
| PASS-SIDE-02 | **When passing on the right is allowed.** WHEN on a MULTI-LANE ROAD, OR on a ONE-WAY ROAD, OR when overtaking a STREETCAR, OR when overtaking a left-turning vehicle, the PASSER **MAY** pass on the right. | PERMISSION | Safe and Responsible Driving › Changing positions › Passing on the right, p. 70 |
| PASS-SIDE-03 | **No sudden pass on the right.** WHEN driving in the leftmost lane behind a slower vehicle, the PASSER **MUST NOT** suddenly change lanes and pass on the right; wait for the slower vehicle to move right. *Note:* The handbook also notes that passing on the right can be more dangerous than passing on the left. | INSTRUCTION | Safe and Responsible Driving › Changing positions › Passing on the right, p. 70 |
| PASS-SIDE-04 | **Right shoulder: left-turning vehicle only.** WHEN the vehicle ahead is turning left AND the right SHOULDER is paved, the PASSER **MAY ONLY** drive on the right SHOULDER to pass it. *Note:* MAY ONLY = permitted in this case and prohibited in every other case. | PERMISSION | Safe and Responsible Driving › Changing positions › Passing on the shoulder, p. 70 |
| PASS-SIDE-05 | **Never on the left shoulder.** WHEN making any PASS, the PASSER **MUST NOT** pass on the left SHOULDER, whether paved or not. | REQUIREMENT | Safe and Responsible Driving › Changing positions › Passing on the shoulder, p. 70 |

## LANE — Passing lanes, climbing lanes and freeways

| ID | Rule | Force | Source |
| --- | --- | --- | --- |
| PASS-LANE-01 | **Passing and climbing lanes.** WHEN on a two-lane section where a PASSING LANE or climbing lane is provided, the DRIVER **MUST** keep to the right-hand lane unless making a PASS; faster vehicles pass in the left lane. | INSTRUCTION | Safe and Responsible Driving › Changing positions › Passing and climbing lanes, p. 70; Diagram 2-48 (p. 70); Traffic Signs and Lights › Signs › Regulatory signs, p. 113 |
| PASS-LANE-02 | **End of passing lane: merge.** WHEN the lane-ending sign for a PASSING LANE or climbing lane is shown and the DRIVER is in the right-hand lane, the DRIVER **MUST** begin to merge safely with traffic in the left-hand lane. | INSTRUCTION | Safe and Responsible Driving › Changing positions › Passing and climbing lanes, p. 70 |
| PASS-LANE-03 | **Freeway: pass in left lanes, then return right.** WHEN driving on a FREEWAY, the DRIVER **MUST** keep right, use the left lanes for passing, and not stay in the far-left lane after passing. *Note:* ‘Traffic should keep to the right’ is advice, but ‘don't stay there’ is an instruction, so the stronger form is recorded. | INSTRUCTION | Safe and Responsible Driving › Freeway driving › Driving along a freeway, p. 79 |
| PASS-LANE-04 | **Trucks on roads with three or more lanes.** WHEN on a high-speed road or FREEWAY with three or more lanes in each direction where trucks are barred from the far-left lane, the DRIVER of a large truck **MUST NOT** use the far-left lane; the lane to its right is the TRUCK PASSING LANE. *Note:* Applies on ‘many’ such roads, not all; the handbook does not say how the restriction is signed. | REQUIREMENT | Safe and Responsible Driving › Changing positions › Passing, p. 69; Safe and Responsible Driving › Freeway driving › Driving along a freeway, p. 79 |

## NIGHT — Passing at night

| ID | Rule | Force | Source |
| --- | --- | --- | --- |
| PASS-NIGHT-01 | **Extra care at night.** WHEN passing at night, the PASSER **SHOULD** pass only if the PASS is necessary and the way is clear, taking extra care. | ADVICE | Safe and Responsible Driving › Changing positions › Passing at night, p. 69 |
| PASS-NIGHT-02 | **Low beams when closing from behind.** WHEN at night, approaching a vehicle from behind, the PASSER **MUST** use low-beam headlights. *Note:* Page 31 exempts the moment of passing from the 60-metre low-beam rule, which is consistent with PASS-NIGHT-03. | INSTRUCTION | Safe and Responsible Driving › Changing positions › Passing at night, step 1, p. 69; Safe and Responsible Driving › Turn on headlights at night and in poor conditions, p. 31 |
| PASS-NIGHT-03 | **High beams once alongside.** WHEN at night, the PASSER has signalled, checked mirrors and BLIND SPOT, pulled out, and is ALONGSIDE the PASSED VEHICLE, the PASSER **MUST** switch on high-beam headlights, UNLESS an oncoming vehicle is within 150 metres (see note). *Note:* The UNLESS clause is inferred by combining p. 69 with the general headlight rule on p. 31; the passing-at-night steps do not mention it themselves. | INSTRUCTION | Safe and Responsible Driving › Changing positions › Passing at night, step 2, p. 69; Safe and Responsible Driving › Turn on headlights at night and in poor conditions, p. 31 |
| PASS-NIGHT-04 | **Night return point.** WHEN at night, all of the front of the PASSED VEHICLE is visible in the rear-view mirror, the PASSER **MUST** signal AND pull back into the right lane. | INSTRUCTION | Safe and Responsible Driving › Changing positions › Passing at night, step 3, p. 69 |

## USER — Passing particular road users and vehicles

| ID | Rule | Force | Source |
| --- | --- | --- | --- |
| PASS-USER-01 | **Cyclists: one metre.** WHEN passing a CYCLIST, the DRIVER of a motor vehicle **MUST** keep at least 1 metre between the vehicle and the CYCLIST, where practical. *Penalty:* A fine and 2 demerit points (p. 40). | REQUIREMENT | Safe and Responsible Driving › Sharing the road with other road users › Sharing the road with cyclists, p. 40; Diagram 2-11 (p. 40) |
| PASS-USER-02 | **Cyclists: change lanes where possible.** WHEN passing a CYCLIST and another lane is available, the PASSER **SHOULD** change lanes to pass. | ADVICE | Safe and Responsible Driving › Sharing the road with other road users › Sharing the road with cyclists, p. 40 |
| PASS-USER-03 | **Cyclists: horn.** WHEN overtaking a CYCLIST, the PASSER **MUST NOT** sound the horn unnecessarily; if the horn is needed, tap it quickly and lightly while still some distance away. | INSTRUCTION | Safe and Responsible Driving › Sharing the road with other road users › Sharing the road with cyclists, p. 40 |
| PASS-USER-04 | **Cyclist lane position.** WHEN the lane is too narrow to be shared safely, the CYCLIST **MAY** use any part of the lane to discourage passing. *Note:* A PASSER can expect this behaviour and not treat it as an error by the cyclist. | PERMISSION | Safe and Responsible Driving › Sharing the road with other road users › Sharing the road with cyclists, p. 39 |
| PASS-USER-05 | **Two-wheelers: no in-lane passing.** WHEN a motorcycle, bicycle, limited-speed motorcycle or moped is positioned to one side of its lane, the PASSER **MUST** pass only by changing lanes; do not take the position as an invitation to pass within the same lane. *Note:* Diagram 2-47 is not captioned; linking it to this paragraph is an interpretation based on what it shows and where it is placed. | INSTRUCTION | Safe and Responsible Driving › Changing positions › Passing, p. 68; Diagram 2-47 (p. 69) |
| PASS-USER-06 | **Two-wheelers turning left.** WHEN turning left behind a motorcycle, bicycle, limited-speed motorcycle or moped, the PASSER **MUST NOT** pull up beside it to turn at the same time; wait for the smaller vehicle to move right before passing. | INSTRUCTION | Safe and Responsible Driving › Changing directions › Turning a corner › Left turns, p. 58 |
| PASS-USER-07 | **Large vehicles: no close cut-in.** WHEN passing a LARGE VEHICLE, the PASSER **MUST NOT** cut in closely in front of it; allow more room than for a smaller vehicle. *Note:* Related hazard (p. 44): a large vehicle's air turbulence may affect control of your vehicle while passing it. | INSTRUCTION | Safe and Responsible Driving › Sharing the road with other road users › Sharing the road with large commercial vehicles, p. 43 |
| PASS-USER-08 | **Long commercial vehicles.** WHEN preparing to pass a vehicle displaying the LCV placard, the PASSER **SHOULD** allow for its extended length (up to 40 metres) and limited speed. | ADVICE | Traffic Signs and Lights › Signs › Other signs › Long commercial vehicle (LCV), p. 128 |
| PASS-USER-09 | **Slow-moving vehicles (farm machinery).** WHEN following a vehicle with a SLOW-MOVING VEHICLE SIGN, the PASSER **MUST NOT** pass until it is safe; stay well back meanwhile. | INSTRUCTION | Safe and Responsible Driving › Sharing the road with other road users › Sharing the road with farm machinery, p. 45 |
| PASS-USER-10 | **Horse-drawn vehicles.** WHEN passing a horse-drawn vehicle, the PASSER **MUST** pass only when safe AND leave as much lateral distance as possible. *Note:* Reason given: passing too closely can startle the horse into changing direction suddenly. | INSTRUCTION | Safe and Responsible Driving › Sharing the road with other road users › Sharing the road with horse-drawn vehicles, p. 46 |
| PASS-USER-11 | **Parked vehicles.** WHEN passing parked vehicles, the PASSER **MUST** watch for doors suddenly opening, or doors open for loading and unloading. | INSTRUCTION | Safe and Responsible Driving › Changing positions › Passing, p. 68 |
| PASS-USER-12 | **Roadside workers and vehicles.** WHEN passing road workers, roadside-assistance or disabled vehicles, surveyors, or maintenance or utility workers, the PASSER **MUST** slow down and pass with caution; if safe, move over a lane. | INSTRUCTION | Safe and Responsible Driving › Dealing with particular situations › Workers on the road, p. 84 |
| PASS-USER-13 | **Animals.** WHEN an animal is on or near the road, the PASSER **MUST** slow down and pass carefully. | INSTRUCTION | Safe and Responsible Driving › Dealing with particular situations › Animals on the road, p. 85 |

## SC — Streetcars

| ID | Rule | Force | Source |
| --- | --- | --- | --- |
| PASS-SC-01 | **Pass streetcars on the right.** WHEN passing a STREETCAR, the PASSER **MUST** pass on the right, UNLESS the PASSER is driving on a ONE-WAY ROAD. | REQUIREMENT | Safe and Responsible Driving › Changing positions › Passing streetcars, p. 71; Diagram 2-49 (p. 71) |
| PASS-SC-02 | **Streetcar stops: 2 metres behind the doors.** WHEN a STREETCAR is stopped and passengers are getting on or off, AND no separate passenger area (safety island or zone) is provided, the DRIVER **MUST** stay at least 2 metres behind the streetcar's rear doors. *Note:* Recorded as REQUIREMENT because the handbook calls it a ‘rule’ in the next sentence (‘This rule does not apply at stops where an area has been set aside...’). | REQUIREMENT | Safe and Responsible Driving › Changing positions › Passing streetcars, p. 71; Diagram 2-49 (p. 71) |
| PASS-SC-03 | **Streetcar safety islands and zones.** WHEN passing a streetcar stop that has a safety island or zone set aside for passengers, the PASSER **MUST** pass at a reasonable speed and be ready for pedestrians to move suddenly or unexpectedly. | INSTRUCTION | Safe and Responsible Driving › Changing positions › Passing streetcars, p. 71; Safe and Responsible Driving › Sharing the road with other road users › Sharing the road with pedestrians, p. 38 |

## STOP — Stopped emergency vehicles, tow trucks and school buses

| ID | Rule | Force | Source |
| --- | --- | --- | --- |
| PASS-STOP-01 | **Stopped emergency vehicle or tow truck: slow down.** WHEN approaching, in the same direction of travel, a stopped EMERGENCY VEHICLE with red (or red and blue) lights flashing, OR a stopped tow truck with amber lights flashing, the PASSER **MUST** reduce speed and proceed with caution. *Penalty:* A fine and 3 demerit points for a first offence; higher fines and up to 6 months in jail for further offences (p. 91). Table of offences: 3 points (p. 148). | REQUIREMENT | Safe and Responsible Driving › Emergency vehicles › Reacting to a stopped emergency vehicle or tow truck, p. 90; Diagram 2-57 (p. 90); Keeping Your Driver's Licence › The demerit point system › Table of offences › Three points, p. 148 |
| PASS-STOP-02 | **Stopped emergency vehicle or tow truck: move over.** WHEN conditions of PASS-STOP-01 apply AND the road has two or more lanes in the PASSER's direction, the PASSER **MUST** move into a lane away from the emergency vehicle or tow truck, if safe, changing lanes well in advance. *Penalty:* As PASS-STOP-01. Table of offences: 3 points (p. 148). | REQUIREMENT | Safe and Responsible Driving › Emergency vehicles › Reacting to a stopped emergency vehicle or tow truck, p. 90; Diagram 2-57 (p. 90); Keeping Your Driver's Licence › The demerit point system › Table of offences › Three points, p. 148 |
| PASS-STOP-03 | **Stopped school bus.** WHEN approaching a stopped SCHOOL BUS with its upper red lights flashing or its stop arm out, from behind, OR from the front on a road without a MEDIAN, the DRIVER **MUST NOT** pass the bus; instead the DRIVER stops (at least 20 metres back when behind it, at a safe distance when facing it) and stays stopped until the bus moves, or its lights stop flashing and the stop arm folds away. *Penalty:* A heavy fine and 6 demerit points for a first offence (p. 54); the registered owner can be given the fines, but not the points (p. 55). Table of offences: 6 points (p. 147). *Note:* The handbook frames this as a duty to STOP; a PASS of a stopped school bus with red lights flashing is therefore prohibited. The amber-light stage (p. 46) requires slowing and preparing to stop. | REQUIREMENT | Safe and Responsible Driving › Stopping › Stopping for school buses, p. 53; Diagram 2-27 (p. 54); Safe and Responsible Driving › Stopping › Stopping for school buses, p. 54; Diagram 2-28 (p. 54); Safe and Responsible Driving › Stopping › Stopping for school buses, p. 55; Keeping Your Driver's Licence › The demerit point system › Table of offences › Six points, p. 147; Diagram 2-18 (p. 46) |

## BEING — Duties of the driver being passed

| ID | Rule | Force | Source |
| --- | --- | --- | --- |
| PASS-BEING-01 | **Do not speed up when being passed.** WHEN another driver is trying to pass, the PASSED DRIVER **MUST NOT** speed up. | REQUIREMENT | Safe and Responsible Driving › Changing positions › Passing › steps for passing, step 4, p. 68 |
| PASS-BEING-02 | **Move right and let faster traffic pass.** WHEN faster traffic wants to pass, the PASSED DRIVER **MUST** move to the right and let it pass safely. *Note:* Sample test question 5 confirms this as the correct answer (key: 5-d); the wrong options were speeding up, moving left, and signalling the other driver not to pass. | INSTRUCTION | Safe and Responsible Driving › Changing positions › Passing, p. 68; Test yourself – Sample knowledge test, question 5 and answer key, p. 170 |
| PASS-BEING-03 | **Being passed on an undivided road.** WHEN on an undivided road, being passed by a driver who has moved into the opposite lane, the PASSED DRIVER **MUST** watch oncoming traffic, move closer to the right side of the lane, and be ready to slow down so the PASSER can get in front sooner. | INSTRUCTION | Safe and Responsible Driving › Changing positions › Passing, p. 68 |
| PASS-BEING-04 | **Clear the truck passing lane.** WHEN driving in the TRUCK PASSING LANE and a truck wants to pass, the PASSED DRIVER **MUST** move into the right-hand lane as soon as possible. | INSTRUCTION | Safe and Responsible Driving › Changing positions › Passing, p. 69 |
| PASS-BEING-05 | **Do not block a pass.** WHEN another vehicle is attempting to pass, the PASSED DRIVER **MUST NOT** drive in a way that prevents the other vehicle from passing. *Penalty:* Listed under ‘Sanctions – dangerous behaviours’ as aggressive driving (p. 150); no specific penalty is given there. | REQUIREMENT | Keeping Your Driver's Licence › Other ways to lose your licence › Sanctions – dangerous behaviours, p. 150 |
| PASS-BEING-06 | **Being overtaken by an emergency vehicle.** WHEN an EMERGENCY VEHICLE approaches from any direction with flashing red (or red and blue) lights, or siren or bell sounding, the DRIVER **MUST** stop immediately, as near as practical to the right-hand curb or edge (on a one-way road or divided highway with more than two lanes, the nearest curb or edge), without stopping on the shoulder. *Penalty:* A fine and 3 demerit points for a first offence (p. 91). *Note:* If already in an intersection preparing to turn, abandon the turn and clear the intersection by going straight, because the emergency vehicle may pass on the side you meant to turn toward (p. 89). | REQUIREMENT | Safe and Responsible Driving › Emergency vehicles › Reacting to an approaching emergency vehicle, p. 88; Diagram 2-56 (p. 90) |

## TOW — Passing while towing a trailer

| ID | Rule | Force | Source |
| --- | --- | --- | --- |
| PASS-TOW-01 | **Passing while towing.** WHEN towing a trailer AND preparing to make, or completing, a PASS, the PASSER **MUST** confirm enough time and room for the slower acceleration and greater length; allow extra room before moving back; do not cut back in too soon. *Note:* Reason given: cutting back too soon can make the trailer sway. | INSTRUCTION | Towing › Passing, p. 167 |
| PASS-TOW-02 | **Holding up traffic while towing.** WHEN towing a trailer AND holding up a line of traffic, the PASSED DRIVER **MUST** signal, pull over, and let the other vehicles pass. *Note:* If a large bus or truck passes and its wind pushes the trailer, do not brake; steer back into position (a slight increase in speed may help). | INSTRUCTION | Towing › Being passed, p. 167 |
