You are tagging every sentence and figure of a driver's handbook. Each tag is picked from a fixed list. You do not rewrite anything, and you do not add words of your own.

## Input

One JSON object per line, one line per paragraph, in reading order:

```
{"para": "mto:para:changing-positions:014", "where": "Changing positions › Passing · ¶3", "sentences": [{"id": "mto:sent:changing-positions:014.1", "text": "Here are the steps for passing a vehicle:"}]}
{"para": "mto:para:changing-positions:019", "where": "Changing positions › Passing · image", "figure": "how to pass another vehicle"}
```

- `where` is the page title and the heading path, then the paragraph's position: `¶3` (third paragraph), `item 2` (second list item), `image` (a figure).
- A text paragraph lists its sentences. A figure has only its alt text, in `figure`.

Read each sentence with its headings and its neighbours. A heading can decide the topic ("Passing", "Stopping for school buses"), and a paragraph ending in a colon leads the list items after it.

## Output

One JSON object per line for every sentence id and every figure's `para` id, in input order, nothing else:

```
{"id": "mto:sent:changing-positions:014.1", "type": "STEP", "modal": "NONE", "caution": 0, "topics": ["passing"], "vague": []}
```

| Key | Values |
|---|---|
| `id` | The sentence id, or a figure's `para` id. |
| `type` | One of `RULE`, `STEP`, `DEFINE`, `FACT`, `CONSEQ`, `META`, `FIGURE` (below). |
| `modal` | One of `MUST`, `MUST NOT`, `MAY`, `SHOULD`, `SHOULD NOT`, `IMPERATIVE`, `IMPERATIVE NOT`, `NONE` (below). |
| `caution` | `1` if it tells the reader to watch out for something, else `0`. |
| `topics` | The topics below that it is about: `[]` or a list of topic names. |
| `vague` | `[]`, or `[["<code>", "<words>"], …]`: vague wording, with words copied exactly from the sentence (below). |

A figure always has `"type": "FIGURE", "modal": "NONE", "caution": 0, "vague": []`; only its `topics` vary.

## Type

- `RULE`: tells someone what they must, must not, may, should or should not do, including advice and cautions. A sign's meaning that tells drivers what to do ("This sign means you must stop") is a RULE.
- `STEP`: one step of an ordered procedure (a numbered or ordered list item, or a sentence inside one), or the lead that introduces such a list. A step that is really a standalone rule or caution is a RULE.
- `DEFINE`: says what a term means or what something is called ("Passing is changing lanes to move past a slower vehicle").
- `FACT`: describes how things are without telling anyone what to do: roads, signs, vehicles, laws, statistics, why something is dangerous.
- `CONSEQ`: a penalty or other consequence ("you can be fined", "six demerit points", "your licence will be suspended").
- `META`: about the book or the reader's study rather than driving: learning objectives, navigation, "For more information visit …", a sample test question or its answer choices, a fragment with no content.
- `FIGURE`: a figure.

## Modal

The force the wording itself gives, as written. Do not apply any reading of the law, and do not turn an imperative into SHOULD or MUST: that is decided later.

- `MUST`: an obligation in the words: must, have to, shall, are required to, it is mandatory, the law requires.
- `MUST NOT`: a prohibition in the words: must not, may not, cannot (as a ban), it is illegal or unlawful or an offence or against the law to, is not permitted, is not allowed, is prohibited.
- `MAY`: a permission: may, can (as permission), are allowed or permitted to.
- `SHOULD`: advice: should, ought to, it is a good idea, it is best or safer to, try to, is recommended.
- `SHOULD NOT`: advice against: should not, it is not a good idea to.
- `IMPERATIVE`: a bare command with no modal word: "Keep right", "Always signal", "Be sure …", "Watch for …", "Avoid …".
- `IMPERATIVE NOT`: a bare negative command: "Do not …", "Don't …", "Never …".
- `NONE`: no instruction: facts, definitions, consequences, "may" or "can" meaning possibility or ability ("roads may be slippery").

When a sentence has several, tag the one of its main instruction.

## Caution

`1` when the sentence tells the reader to watch out, be careful, be prepared, look out or be alert for something; `0` otherwise.

## Topics

A sentence or figure is about a topic when the topic's scope below covers it, read together with its headings. A sentence that a rule on the topic needs (the lead of a list of passing steps, a penalty for a passing offence, a definition used by passing rules) is about the topic too. Most sentences are about none of them.

- `passing`: Passing (overtaking): a driver moving past another vehicle going the same way, whether that vehicle is travelling, stopped in traffic or parked, and everything that decides whether, where, when and how a driver may do so, including lane use for passing, duties that make passing a stopped vehicle illegal (such as having to stop for it), and what a driver who is being passed should do. "Pass" used only to mean going by a person, an animal, a work zone or another hazard is not this topic.

## Vague wording

Copy the words exactly as they appear in the sentence (same case, same punctuation), as short as still makes the point. One entry per vague piece; none is fine.

| Code | When | Examples |
|---|---|---|
| `J` | Judgment term: needs human judgment, no threshold | safe, safely, enough, sure, in doubt, reasonable, proper, plenty of room, as soon as you can, carefully, too fast, well before |
| `M` | Unclear legal force: cannot tell law from advice; a "never" or "don't" that may be law; a "must" that reads like advice | "Don't pass moving snow plows under any conditions" |
| `S` | Hedged scope: a hedged quantifier | many, most, some, usually, often, generally, in some areas |
| `R` | Unclear reference or role | "these areas", "the lane next to it", "they" with several candidates, unclear who must act |
| `D` | Implicit default: the sentence depends on something it does not state | "only to pass a vehicle turning left" presupposes driving on the shoulder is otherwise not allowed |
| `G` | Goal and means differ: one place prohibits the goal, another the means | "passing left of a centreline" next to "passing" |

## Examples

```
{"id": "ex1", "type": "DEFINE", "modal": "NONE", "caution": 0, "topics": ["passing"], "vague": []}
```
"Passing is changing lanes to move past a slower vehicle."

```
{"id": "ex2", "type": "RULE", "modal": "IMPERATIVE NOT", "caution": 0, "topics": ["passing"], "vague": [["M", "Don't pass moving snow plows under any conditions"]]}
```
"Don't pass moving snow plows under any conditions."

```
{"id": "ex3", "type": "RULE", "modal": "IMPERATIVE", "caution": 1, "topics": ["passing"], "vague": []}
```
"Watch for people suddenly opening doors of parked vehicles." (under the heading "Passing parked vehicles")

```
{"id": "ex4", "type": "RULE", "modal": "MUST", "caution": 0, "topics": ["passing"], "vague": []}
```
"You must stop whenever you approach a stopped school bus with its upper alternating red lights flashing."

```
{"id": "ex5", "type": "CONSEQ", "modal": "NONE", "caution": 0, "topics": [], "vague": []}
```
"If you accumulate too many demerit points, your driver's licence can be suspended."

```
{"id": "ex6", "type": "FACT", "modal": "NONE", "caution": 0, "topics": [], "vague": [["S", "Many high-speed roads"]]}
```
"Many high-speed roads have more than one lane in each direction."

```
{"id": "ex7", "type": "META", "modal": "NONE", "caution": 0, "topics": [], "vague": []}
```
"For more information, visit ServiceOntario."

Be consistent rather than clever. When two tags are close, pick the closer one; add a vague entry only when the words themselves are vague.
