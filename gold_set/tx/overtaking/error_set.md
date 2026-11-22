# Error set: confirmed error types

Kinds of error that were confirmed and fixed at triage while building the overtaking gold set (steps
a0–a3 and b0–b3). Examples give the step and finding id: a0 = `a0_freeform_report.md` (M = major; V,
C, G, F, N = minor), a1 = `a1_format_report.txt`, S2 = `a2_atomic_report.md`, S3 =
`a3_aggregate_report.md`; b0 = `b0_freeform_report.md` (m = minor), b2 S2 = `b2_atomic_report.md`,
b3 S3 = `b3_aggregate_report.md`. Rule ids are as they were at that step. No rule was renumbered:
new rules were added at the end of their groups.

The companion list of reported errors that were rejected is `allow_list.md`.

## Faithfulness: the rule says something the handbook does not

- **A duty turned into a permission.**
  - a0 M2: 7.24's "Always keep to the right side of the road except when" became GEN-07's "MAY leave
    the right side of the road". Now the keep-right duty, with 7.25–7.27 as its exceptions.
- **A rule widened beyond the handbook's context.**
  - a0 M5: GEN-09 and BEING-09 come from the freeway section (10.12, 10.13), but applied to every
    HIGHWAY, which the vocabulary defines as any public way (16.78). Now limited to a FREEWAY.
  - S2-053: USER-06 applied to "passing a TRUCK or other vehicle". 10.113 is about passing a truck,
    and its "the other vehicle" is the truck. Now "passing a TRUCK".
- **A general rule narrowed to one situation.**
  - S2-063: USER-11 put 10.125's "Never cross behind a truck preparing to back up" under the
    loading-area condition of the next sentences. Split: USER-11 keeps the wait before passing, and
    USER-17 holds the general ban.
- **Words added that the handbook does not use.**
  - a0 V1: PASS's definition added "and then returning in front of it". The glossary (16.106) does
    not have it, and it does not fit passing on the right or on a shoulder.
- **A penalty misstated.**
  - S2-046, S2-047: USER-01 and USER-02 said serious injury "is a Class A misdemeanor or state jail
    felony". The felony applies only after a previous conviction for the same offence (5.83, 5.84).
  - b2 S2-039, S2-041: USER-01 and USER-02 said "2nd within 5 years"; 5.82 says "2nd conviction and
    every conviction after". Now "2nd and later convictions within 5 years".

## Conditions and exceptions

- **A condition that is not a fact** ("especially …", "including …").
  - a0 G5: USER-05 ("especially at night", now in the note), BEING-01 ("including a TRUCK"), USER-09
    ("including when trying to reach an exit …").
- **A condition that repeats the action.**
  - a0 G2: PROC-07's "WHEN returning to the right lane after passing …, the PASSER MUST … return to
    the right lane" became "WHEN the PASSER has overtaken the vehicle being passed …".
  - S2-055: USER-07's "WHEN returning in front of a TRUCK …, the PASSER MUST NOT move back into the
    lane" became "WHEN passing a TRUCK, … MUST NOT move back into the lane in front of the TRUCK".
- **An exception that cannot hold while the condition holds.**
  - a0 G6: USER-02's "OR the red lights are no longer flashing", under "WHEN a school bus is
    displaying alternately flashing red lights". The condition now describes the stop: "WHEN the
    DRIVER has stopped for a school bus …".
- **An exception that refers to other rules instead of stating a fact.**
  - a0 M2: GEN-07's "UNLESS a condition under which driving on the left side of the road is
    prohibited applies".
- **A missing exception.**
  - S2-027: MARK-01's permission to cross a BROKEN LINE did not exclude a combined line with a SOLID
    YELLOW LINE on the PASSER's side (6.200). Now UNLESS that is so.
- **An exception that leaves out the limits the handbook puts on it.** The rule should read on its
  own.
  - b2 S2-015, S2-017: PROC-06's and PROC-07's "UNLESS passing on a paved shoulder" (added in b0 m1)
    did not say when that is allowed. Both now name 7.45's cases: the vehicle being passed is
    slowing or stopped on the main traveled portion of the HIGHWAY, disabled, or preparing to make a
    left turn.
- **A condition that does not say where a ban applies.**
  - S2-036: SIGN-01's "a … sign applies to the DRIVER's direction" did not say that the ban holds in
    the zone the sign marks; the pennant gives advance warning (6.50). Now "in a NO-PASSING ZONE
    marked for the DRIVER's direction by …".
- **A condition whose scope is unclear.**
  - a0 G1: AND and OR mixed with no grouping (MARK-02), or grouped with brackets the grammar does
    not have (SIDE-01).
  - a0 G7: "another vehicle is passing the DRIVER" (BEING-01, 02, 04) did not say that it is the
    DRIVER's vehicle; PROC-02 dropped 7.35's "passing you".
  - b0 m3: the same fix in BEING-05 and BEING-06 ("a TRUCK is passing the DRIVER's vehicle"), which
    a0 G7 missed, and in PROC-02 ("passing the PASSER's vehicle"), which reopened G7's wording
    (`allow_list.md`, Re-raising a settled triage).

## Strength (force and modal)

- **A plain command recorded as ADVICE.**
  - a0 M3: GEN-01's "Be patient and wait" (7.29) went to INSTRUCTION / MUST.
- **The stronger of two wordings not recorded.** The task says to record the stronger one and say so
  in the note.
  - a0 M4: SIGN-02's warning signs say "do not pass", and disobeying a warning sign is a violation
    with a fine (6.56, 6.266, 6.267). Now REQUIREMENT, with the fine as its penalty.
  - b2 S2-030: SIGN-02's note did not say so. It now says that the sign descriptions word the rule
    as a plain command and that disobeying a warning sign is a violation with a fine.
- **MAY where the handbook states the "only".**
  - a0 G3: SIDE-02's paved-shoulder case is a list item under 7.42's "only when". Now MAY ONLY, with
    7.42's safety condition added.
- **A note that gives the wrong reason for the strength.**
  - S2-025: LOC-05's note said the rule was raised to REQUIREMENT partly because it is "stated
    twice". Repetition does not raise strength; the note now rests it on the regulatory sign
    (6.149-f1) and 6.115.

## Granularity

- **Two duties with different scopes under one condition** → split.
  - S2-063, S2-064 (USER-11's "…, and never cross behind it" inside a MUST action; now USER-11 and
    USER-17).

## Grammar and wording

- **A second modal inside an action.**
  - a0 M1: "MUST NOT …, and must …" (GEN-06, USER-09, USER-13). Reworded to the positive-first,
    negated-last pattern.
- **MAY ONLY on the verb, which can be misread.**
  - a0 G3: SIDE-01's "MAY ONLY PASS on the right" read as "may pass only on the right". The note now
    gives the reading.
- **The prompt example's wording instead of the handbook's.**
  - a0 G8: MARK-01's "at the left of the PASSER's lane". Now from 6.187: "You may cross a broken
    line when passing".
- **A reason written into the action.**
  - a0 N1: USER-12's "as the other driver may drift in front" moved to the note.
- **A referent that is unclear or missing.**
  - S2-019: PROC-05's "comes within 200 feet" dropped 7.36's "of you"; now "of the PASSER".
  - S2-041: SIGN-03's "pass on either side of it" (the sign, or the island?); now "of the traffic
    island or obstruction".
  - S2-055: USER-07's "the lane"; now "the lane in front of the TRUCK".
  - S2-082, S2-084: BEING-05's and BEING-07's "far side" did not say far from what; now "farther
    from the passing TRUCK" and "farther from the passing vehicle".
  - b2 S2-050: USER-09's note said cutting in "removes the driver's cushion of safety", where DRIVER
    is the actor; now "the truck or bus driver's cushion of safety".
- **Alternatives in an action without the handbook's grouping word.**
  - b2 S2-047: USER-09's "slow down and exit or stay behind the TRUCK or bus, and not cut into …"
    now takes 10.129's "either": "either slow down and exit, or stay behind the TRUCK or bus, and
    not cut into the open space in front of it".
- **Two passages' wording mixed in one action.**
  - S2-073: USER-15 and USER-16 said "the speed limit" (9.30) and "the posted speed limit" (5.71) in
    the same action; now "posted" in both places.
- **A title that does not match the statement.**
  - S2-063 (USER-11, after the split); S3-004 (SIDE-01, when narrowed to a traffic lane).

## Vocabulary and terminology

- **A verb written as the CAPS term.**
  - a0 V1: PASS was defined as a verb and capitalized as a verb in 21 statements. The verb is now
    lowercase; the noun PASS stays capitalized.
- **A vocabulary term written in lowercase where its defined meaning is intended.**
  - a1: "driver" or "drivers" (eight times), "highway", "truck". Where capitalizing would misname
    the person, the phrase was reworded: "the DRIVER of the school bus" (USER-02), "the DRIVER of
    the TRUCK" (USER-05), "the vehicle of a DRIVER" (USER-12), "the PASSER" (BEING-04).
  - a1: MARK-03's "highway" became HIGHWAY, not FREEWAY, because 6.196 and 6.197 are under Pavement
    Markings, not the freeway section.
- **A definition that builds in meaning, position or use.** Define the thing itself.
  - a0 V2: BROKEN LINE ("which permits passing …"), SOLID YELLOW LINE ("marks a NO-PASSING ZONE"),
    DOUBLE YELLOW LINE ("on a multi-lane highway"). Now self-made definitions with empty evidence;
    the meanings stay in MARK-01 to MARK-03.
- **A definition that states a fact about the thing instead of what it is.**
  - a0 V3: CYCLIST's "a vehicle with the rights and responsibilities of a driver" (10.176). Now "A
    person riding a bicycle.", self-made with empty evidence; 16.14 defines a bicycle, not a
    cyclist.
- **A setting that needs its own term.**
  - a0 M5: FREEWAY, defined from 10.13, because HIGHWAY is the legal term for any public road.
- **A definition taken from the handbook but cited with empty evidence.**
  - S3-010: SERVICE VEHICLE copies 9.29's list of vehicles; it now cites 9.29, as FREEWAY cites
    10.13. This reversed S2-072 and S2-078.
- **The same actor written two ways.**
  - b3 S3-006: BEING-07's "DRIVER of a TRUCK" and BEING-10's "DRIVER of the TRUCK". Both now use
    "DRIVER of a TRUCK", and BEING-10's condition no longer repeats the actor.

## Citations

- **A list item cited without the line that introduces it.** Applied to every rule and vocabulary
  entry citing a list item.
  - a0 C1: 7.42 on SIDE-02; 7.17 on MARK-02, SIGN-01 and NO-PASSING ZONE; 2.293 on USER-01 and
    USER-02.
- **A cited block that does not support the rule.**
  - a0 C2: the passing diagram 7.40 on PROC-01 (following distance); 10.115 on BEING-07 (its
    truck-driver sentence is about signalling after the pass).
- **A supporting block not cited.**
  - a0 C3: 6.115 (drivers must obey regulatory signs as traffic laws) on LOC-05; 10.48 on GEN-06;
    6.56, 6.266 and 6.267 on SIGN-02 (a0 M4).
  - S2-010, S2-087: 10.13 on GEN-09 and BEING-09. Their FREEWAY setting comes from that opening
    paragraph of the section; the headings above 10.23 and 10.34 say "highway", not freeway.
  - S2-074, S2-075: 9.31 and 5.69 on USER-16. Its one-lane condition rests on their lane condition
    for moving over.

## Vague terms

- **A vague word or phrase kept in the statement but not listed.** This is the most common error.
  Examples:
  - a0 (vague terms): "safely" (USER-03, BEING-03), "as far to the right as possible" (BEING-03),
    "near a MOTORCYCLE" (USER-13).
  - a0 G3: "conditions permit doing so safely" (SIDE-02).
  - "the proper signal" (S2-002), "linger" (S2-007), "see ahead clearly" (S2-013), "the roadway is
    clear" (S2-015).
  - "hill" and "curve" (S2-024), "the curve or winding section ahead" (S2-039).
  - "the lane is clear" (S2-050), "having passed a TRUCK" (S2-057).
  - "the open space in front of it" (b2 S2-049).
- **An explanation that does not say what the words leave open** (task.md).
  - b2 S2-016: PROC-06's "safely cleared" now reads "no gap or distance given; the only concrete
    check is seeing the passed vehicle in the rearview mirror".

## Notes

- **An inference or reading not stated in the note.**
  - S2-023: LOC-01's "left side of the road" is the half used by oncoming traffic, not the left lane
    of the DRIVER's own direction.
  - S2-053: USER-06's source says "the other vehicle" (10.113), meaning the truck being passed.
  - S2-071, S2-076, S2-077: USER-15 and USER-16 apply the officer exception (5.68) and the
    under-25-mph case (5.71), which are stated only for emergency vehicles, to every SERVICE
    VEHICLE.
  - S2-010, S2-087: GEN-09's and BEING-09's FREEWAY setting comes from 10.13.
  - b2 S2-044: S2-056 made USER-07's note say that the flash does not replace the mirror check,
    without saying that this is a reading of 10.114. The note now says so.
- **A note that misstates its source.**
  - a0 N2: USER-01's note said children cross; diagram 5.73 shows pedestrians beside the bus.
  - S2-008: GEN-06's note said 10.48 states the rule "again"; 10.48 states it more broadly, for all
    driving.
  - S2-025 (see Strength).
  - b2 S2-001: GEN-01's note said improper passing "often results in deadly head-on crashes"; 7.29
    says such crashes "often result in head on crashes and can be deadly". The note now follows
    7.29.
- **A note that can be read as an alternative to the rule's condition.**
  - S2-056: USER-07's note on the truck driver flashing the truck's lights now says that this does
    not replace seeing the entire front of the truck in the rearview mirror.
- **The handbook's reason missing from the note.**
  - S2-065: 10.125's reasons, split between USER-11 (the road is temporarily blocked) and USER-17
    (the truck's blind spot).
  - b2 S2-054: USER-13 (the motorcycle is entitled to a full lane and may need the room to maneuver
    safely).
- **A handbook detail that limits the rule missing from the note.**
  - S2-037: 7.17 and 7.19 word SIGN-01's ban more broadly, as driving on the left in a No Passing
    Zone.
  - S2-072: 9.31's move-over list leaves out utility service vehicles (USER-15).
  - b2 S2-024: the same for MARK-02 (7.17, 7.19).
- **A rule id in a note written without its topic.**
  - S2-049 (USER-01 → PASS-USER-01), S2-085 (BEING-10 → PASS-BEING-10); b0 m4 (GEN-07's note: LOC-01
    to LOC-04, MARK-02 and SIGN-01).
- **A missing link to a related rule**, where one rule's scope depends on another.
  - a0 M2: GEN-07 → LOC-01 to LOC-04, MARK-02 and SIGN-01, which limit when the left side may be
    used.
  - a0 M5: GEN-09 ↔ SIDE-01.
  - a0 G6: USER-02 → USER-01 (5.78's exceptions).
  - a0 M6.2: BEING-07 → BEING-10.
  - b0 m1: PROC-06 → SIDE-02 (passing on a paved shoulder, 7.45).
  - b2 S2-020: MARK-01 → MARK-02 (6.187's "Do not cross the line if it is not safe or it is a solid
    yellow line").

## Coverage: rules the set left out

- **A rule about driving past a stopped vehicle.**
  - a0 M6.1: slow down or move over for a stopped emergency, tow, utility or TxDOT vehicle
    (9.29–9.31, 5.68–5.71). Added as USER-15 (two or more lanes) and USER-16 (one lane), with the
    new SERVICE VEHICLE term.
- **A rule hidden in another rule's note.**
  - a0 M6.2: the truck driver should signal before returning after a pass (10.115). It was only in
    BEING-07's note. Added as BEING-10.
- **Passing a hazard other than a vehicle.**
  - a0 M6.3: the two-arrow sign (6.98). Added as SIGN-03.
  - a0 M6.4: barricade stripes show the side on which to pass (6.243–6.249). Added as SIGN-04.
- **A general ban lost when it was folded into a narrower rule.**
  - S2-063: "Never cross behind a truck preparing to back up" (10.125). Added as USER-17.

## Conflicts between rules

- **A MAY ONLY permission that forbids what a sibling permission allows.**
  - S3-004: SIDE-01's "MAY ONLY pass on the right" (on a one-way or wide road) forbade the
    paved-shoulder pass that SIDE-02 allows. SIDE-01 now covers passing on the right in a traffic
    lane, and SIDE-02 the shoulder.
- **A duty with no exception for what a sibling permission allows.**
  - b0 m1: PROC-06 required passing on the left on a two-lane road, where SIDE-02 allows passing on
    a paved shoulder (7.45). The handbook names this case, so it is an exception, not a tension the
    handbook leaves open: PROC-06 and PROC-07 got "UNLESS passing on a paved shoulder", with 7.45
    cited. b2 S2-015 and S2-017 then wrote 7.45's cases into the exception (Conditions and
    exceptions).
- **Two rules that pull different ways, with no note saying how they relate.**
  - a0 M5: GEN-09 vs SIDE-01 on a freeway. Notes in both now link them; the handbook does not say
    which applies (`allow_list.md`, Tensions the handbook leaves open).
