You will read part of a driver's handbook and write down its rules of the road.

## Why

The rules will be used to guide and check an AI driving model: a vision-language-action model that
sees the road through cameras and decides how to drive. A rule helps it when it says what a driver
must or should do, or must not do, in a situation the model can recognize: a sign, a signal, a
road marking, the layout of the road, another road user, the weather or light, or the state of
the vehicle. People will check every rule against the handbook, so each one must point to the
exact handbook text it comes from.

## The handbook text

The handbook is given as HTML: a table of contents, then each page as an <article>. Every heading,
paragraph, list item, table row and figure has an id such as "10.22" (block 22 of page 10).
Images come right after their <img> tag. Read them together with the text around them, because a
sign, a marking or a diagram is often part of a rule.

## What to extract

A rule says what a driver must, must not, should, should not or may do, and in what situation.
Extract every rule the pages state, including:
- advice ("check your blind spot") as well as obligations ("you must stop");
- conditions and exceptions, kept with the rule they belong to;
- rules shown by a sign, a road marking, a diagram, a table or a list.

Leave out text that states no rule: introductions, history, statistics, explanations of why a
rule exists, and contact details. Rules about licences, insurance, fees and tests are not rules of
the road. Leave those out too.

## How to write each rule

- Write one rule per entry, as one plain sentence: who does what, in what situation.
- Keep the handbook's strength. Use "must" or "must not" for obligations and prohibitions,
  "should" or "should not" for advice, and "may" for permissions.
- Make each rule stand on its own. Name the situation; do not write "in this case" or "as above".
- Keep separate the rules that apply to different situations, and do not split one rule into
  pieces.
- Do not add rules the handbook does not state, even rules that are true elsewhere.

## Evidence

For each rule, give the handbook text it comes from: the block id, and a quote copied word for
word from that block. Quote one or more whole sentences, or the part of a sentence that states the
rule. If a rule draws on several blocks, such as a rule and its exception or a list and the line
that introduces it, give one evidence entry per block. Quotes are checked against the handbook
automatically, so copy them exactly.

## Before you answer

Go through the pages again, block by block, and check that every rule they state is in your list.
Leaving out a rule is worse than writing one rule twice.
