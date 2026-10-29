Records of the prompts the team gave Claude, kept as written at the time. Paths in them are the paths of that time: since 23 October 2026 the handbooks are in `handbooks/{mto,ca,tx}/`, the scrapers in `scrapers/`, and the first PDF-based Ontario drafts in `legacy/` on the branch `archive/rule-pipeline`.

Used on Claude Opus 5.5 medium web view to generate Ontario passing rules.md and ontario_passing_rules.yaml:
```
take a look at the uploaded pdf Ontario Driver's Handbook, I want to create a set of formal rules about passing from the information in the handbook, the rules should have a defined format and vocabulary and the rules should have proper source attribution to the text section and/or diagram where the information comes from
```

Prompt used to convert pdf page citations into local scraped HTML citations:
```
take a look at C:\Users\hhguo\Desktop\Drive-Rule-Extraction-Bench\Ontario passing rules.md and C:\Users\hhguo\Desktop\Drive-Rule-Extraction-Bench\ontario_passing_rules.yaml, it's currently citing sources from the pdf version of the rule book C:\Users\hhguo\Desktop\Drive-Rule-Extraction-Bench\The Official Ministry of Transportation (MTO) Driver’s Handbook _ ontario.ca.pdf, I want to convert the source attribution citations into the local scraped html format: C:\Users\hhguo\Desktop\Drive-Rule-Extraction-Bench\mto_drivers_handbook, C:\Users\hhguo\Desktop\Drive-Rule-Extraction-Bench\scrape_mto_handbook.py was the script that handled the scraping 
```

Claude response:
```
I've switched every citation in both files from PDF page numbers to links into the local HTML copy in mto_drivers_handbook/. All 53 links and image paths resolve to real files and anchors, and no PDF page references remain. Nothing is committed yet.

  YAML (ontario_passing_rules.yaml)
  - Each source's page: 67 is now href: changing-positions.html#passing, the file plus the nearest heading that has an anchor.
  - Each diagram_page is now diagram_href (the section the diagram is in) plus diagram_image (e.g. images/2-35.jpg).
  - The header now records the scrape: base folder, the ontario.ca base address, scrape date 2026-10-06, and how citations work.
  - Vocabulary basis fields and the page numbers inside penalties and notes now point to sections too.
  - I loaded and re-saved the file with the same YAML settings that produced it, so nothing else changed.

  Markdown (Ontario passing rules.md)
  - The Source column is now clickable links, e.g. [Safe and Responsible Driving › Changing positions › Passing](mto_drivers_handbook/changing-positions.html#passing).
  - The vocabulary table, penalties and notes link the same way.
  - The intro, the "Source" field description and the "Citation style" paragraph now describe the HTML citations instead of PDF pages.

  How I matched them: a script searched the HTML for every quoted sentence and checked that it sits in the cited section. Every quote was found. Some location paths changed to follow the HTML headings:
  - Emergency vehicles → under Dealing with particular situations
  - Turn on headlights… → under Getting ready to drive
  - Table of offences → no longer under The demerit point system
  - Snow › Whiteouts → Whiteouts
  - Turning a corner › Left turns → Left turns
  - Towing and Test yourself → under Your Vehicle, as the table of contents nests them

  Two things to check:
  1. Pavement-marking diagram numbers changed. In the HTML each caption comes after its image. That makes the solid-line diagram 3-2 and the broken-line diagram 3-3, not 3-1 and 3-2 as cited before. 3-1 is the general yellow/white lines picture. I renumbered PASS-MARK-01 and -02 and rewrote their
     diagram descriptions after looking at the images. I couldn't open the PDF to check its numbering, so look at this one yourself.
  2. Links only reach top-level sections. Only h2 headings have anchors in the scraped HTML. Lower headings such as Fog › Tips… › DON'T, and steps such as "step 3", appear only in the citation text. Pavement markings has no section anchors at all, so those links go to the page.
```

## California and Texas handbooks (Claude Code, Opus 5.5, 2026-10-20)

Request to Claude Code, run on the lab server in this repo:
```
So far we have use the MTO driver's handbook as the starting example, and we want to extend the current extraction approach to
1. include more driver's handbook, such as san fran California and austin Texas
...
You can first download both the full handbooks to this repo as you did for mto drivers handbook
```

Claude found that both handbooks are state-wide (there is no San Francisco or Austin handbook), that California publishes its handbook as web pages plus a PDF, and that Texas publishes only a PDF. It gave each handbook to a separate Claude subagent with the briefs below, then checked their results. The briefs are abridged: the parts about this server's Python setup and about how to report back are left out.

<details>
<summary>Brief for the California subagent</summary>

```
TASK: write `scrape_ca_handbook.py` at the repo root. It downloads the California DMV Driver Handbook
(https://www.dmv.ca.gov/portal/handbook/california-driver-handbook/) into `ca_drivers_handbook/` in the SAME
clean format as the MTO copy. Then run it and verify the result.

Read `scrape_mto_handbook.py` and one output page, for example `mto_drivers_handbook/changing-positions.html`,
before you start. Keep every content page, in the handbook's own order. The "-cont" pages are separate web
pages, so keep them as separate files, titled the way the site titles them.

Output format. Match the MTO copy so one downstream segmenter can read all handbooks:
- `ca_drivers_handbook/index.html` (cover and contents), one `<slug>.html` per page, `images/`, and `style.css`.
  Reuse the MTO script's page template, CSS, pretty-printer, TOC sidebar, pager and "On this page" approach.
  You may import from `scrape_mto_handbook.py` or copy the helpers, but do not change that file.
- Each page has `<main><h1>Title</h1>`, the pager, the "On this page" nav, then `<article class="content">`
  holding ONLY the handbook content. Use clean h2/h3/h4, p, ul/ol/li, table, and img inside p. Captions go in
  the following p, as in MTO. Text inside a paragraph stays on one line.
- Unlike MTO, give EVERY heading (h2, h3, h4) a stable slug id, so citations can link to subsections. Keep the
  heading hierarchy faithful to the site.
- Strip the site chrome: header, footer, breadcrumbs, menus, scripts, tracking, feedback widgets, "back to top"
  links, inline style and data-* attributes. Expand any accordion or tab content so all text is present.
- Download every content image to `images/`, keeping its alt text. Rewrite links between handbook pages to the
  local files (with #anchors where possible). Make other links absolute.
- Add the Updated/Source line as MTO does. Use the page's last-updated date if the site shows one, and record
  the scrape date.

Verification (required; report the numbers):
1. Every page's visible text matches the live content word for word, after whitespace normalisation. Compare
   the extracted article text against a fresh independent extraction of the live page's main content region.
2. Every image referenced exists locally and opens.
3. All internal links resolve to existing files and anchors.
4. Spot-check that the passing-related content is fully present, and list where it lives.

Constraints: do not modify existing files in the repo, do not run git add or commit. Be polite to the server:
sequential requests with a small delay.
```
</details>

<details>
<summary>Brief for the Texas subagent</summary>

```
TASK: the Texas Driver Handbook is published only as a PDF: https://www.dps.texas.gov/internetforms/Forms/DL-7.pdf
(about 29 MB). Write `scrape_tx_handbook.py` at the repo root. It downloads that PDF and converts it into
`tx_drivers_handbook/` in the SAME clean HTML format as the MTO copy. Then run it and verify the result.

Output format. Match the MTO copy so one downstream segmenter can read all handbooks:
- Save the PDF as `tx_drivers_handbook/source/DL-7.pdf`. The script should skip the download if the file is
  already there.
- `tx_drivers_handbook/index.html` (cover and contents), one `<slug>.html` per chapter (use the PDF's chapter
  structure and bookmarks/outline if present), `images/`, and `style.css`. Reuse the MTO script's page
  template, CSS, pretty-printer, TOC sidebar, pager and "On this page" approach.
- Each page has `<main><h1>Chapter title</h1>`, the pager, the "On this page" nav, then
  `<article class="content">` holding ONLY handbook content, in clean h2/h3/h4, p, ul/ol/li, table, img.
- Give EVERY heading a stable slug id. Detect heading levels from font size and weight, and from the PDF
  outline. Keep the hierarchy faithful.
- Rebuild the reading order properly: join lines into paragraphs, join paragraphs split across page breaks or
  columns, turn bullets into list items, and de-hyphenate words broken at line ends. Drop running headers and
  footers and page numbers. For traceability, put `data-pdf-page="N"` on every content block element.
- Figures: extract embedded images, or render figure regions to PNG, into `images/`. Each img gets an alt drawn
  from its caption or nearby label (the PDF has no alt text; say so in `data-alt-source`). Keep each sign image
  with its label text.
- Tables (sign tables, penalty tables) stay HTML tables.
- Add the Updated/Source line: the handbook's revision date, the PDF URL, and the conversion date.

Verification (required; report the numbers):
1. Text coverage: compare the bag of words of all article text against the PDF text, excluding running
   headers, footers and page numbers. Report the coverage and list any missing passages.
2. Reading order: spot-check 5 multi-column or page-break spots.
3. Every image referenced exists.
4. Spot-check that the passing-related content is fully and correctly present, and list where it lives.

Constraints: do not modify existing files in the repo, do not run git add or commit.
```
</details>

Claude response (summary):
```
California: ca_drivers_handbook/ has 23 pages and 74 images, plus the DMV's PDF edition in
source/DL-600.pdf. Checked against dmv.ca.gov on 2026-10-20: all 23 pages match word for word
(21,413 words), the heading outline matches, all 74 images are byte-identical, and none of the 955
internal links is broken.

Texas: tx_drivers_handbook/ has 21 pages (cover and contents, Chapters 1-14, Appendices A-E, back
cover) and 203 images rendered from the PDF, plus the PDF itself in source/DL-7.pdf. Reading order and
heading levels come from the PDF's tags. Every block records its PDF page. The HTML holds 98.2% of the
PDF's words; the rest are chapter titles (in each page's <h1>) and table headers the PDF repeats on
every page. No run of four or more words is missing on any page.
```
