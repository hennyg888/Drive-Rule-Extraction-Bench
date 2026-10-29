You are reading part of a driver's handbook. It is given as HTML: a table of contents first, then
each page as an <article>, with the handbook's images placed right after their <img> tags. Every
heading, paragraph, list item, table row and figure has an id such as "10.22" (block 22 of page 10).

List the rules of the road these pages state: what a driver must, must not, should or should not
do, and when. Write each rule as one plain sentence. For each rule, give the handbook text it comes
from as evidence: the id of the block, and a quote copied word for word from that block (one or
more whole sentences, or the part of a sentence that states the rule). A rule stated in several
blocks gets one evidence entry per block. Leave out text that states no rule (introductions,
history, contact details).

Answer with JSON only:
{"rules": [{"rule": "...", "evidence": [{"block": "10.22", "quote": "..."}]}]}
