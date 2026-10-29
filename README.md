# Drive-Rule-Extract-Bench

This is a dataset and framework for benchmarking how well visual language models (VLMs) can extract formalized rules of the road from a driver's handbook. It tests for accuracy, coverage, and correct attribution to source materials as input modalities vary (E.g. text-only, text-and-image, whole page as image). 

Project for VLM CS886 F26 by Michael Lee and Henry Guo.

## Handbooks

The three handbooks are kept as local HTML pages with their images. These HTML copies are the source of truth: everything given to a model is built from them, in their page order with the images where they appear. Each handbook folder also keeps the published PDF, for people to read; the PDFs are not used as model input for now.

| Handbook | HTML pages and images | PDF | Made by |
|---|---|---|---|
| Official MTO Driver's Handbook (Ontario) | `handbooks/mto/`: 30 pages, 241 images | `handbooks/mto/source/MTO-drivers-handbook-ontario.ca.pdf` | `scrapers/scrape_mto_handbook.py`, from the ontario.ca web pages |
| California Driver's Handbook, DL 600 (Rev. 6/2025) | `handbooks/ca/`: 23 pages, 74 images | `handbooks/ca/source/DL-600.pdf` | `scrapers/scrape_ca_handbook.py`, from the dmv.ca.gov web pages |
| Texas Driver Handbook, DL-7 (revised January 2026) | `handbooks/tx/`: 21 pages, 203 images | `handbooks/tx/source/DL-7.pdf` | `scrapers/scrape_tx_handbook.py`, from the DPS PDF (Texas publishes no web version) |

The handbooks are state- and province-wide: San Francisco and Austin drivers use the California and Texas handbooks.

All three HTML copies have the same layout, so one program can read any of them. The handbook text is inside `<article class="content">`, with headings, lists and tables as ordinary HTML and every image in the folder's `images/`. Open `index.html` in each folder to browse it.

## Handbook analysis

What each handbook gives a model: the text and images inside the pages' `<article class="content">`. A text block is a paragraph, a list item or a table row.

| | Ontario (MTO) | California (DMV) | Texas (DPS) |
|---|---:|---:|---:|
| Pages | 30 | 23 | 21 |
| Headings | 454 | 229 | 295 |
| Text blocks (paragraphs, list items, table rows) | 1,911 | 1,023 | 1,788 |
| Sentences | 3,587 | 1,695 | 2,711 |
| Words | 53,789 | 21,463 | 41,814 |
| Text tokens | 66,692 | 27,563 | 53,935 |
| Words per block: median / 90th percentile / max | 18 / 63 / 195 | 14 / 41 / 207 | 16.5 / 49 / 222 |
| Blocks with more than 3 sentences | 218 | 74 | 81 |
| Blocks with more than 80 words | 77 | 15 | 40 |
| Images (distinct files) | 245 (241) | 74 (74) | 203 (203) |
| Image median size (px) | 170 x 104 | 228 x 198 | 138 x 138 |
| Image pixels (millions) | 7.4 | 5.7 | 10.3 |
| Image tokens (estimate) | 9,310 | 7,213 | 13,254 |
| Images whose alt text says nothing specific | 87 | 9 | 0 |
| Text share of all tokens | 88% | 79% | 80% |

Text tokens counted with the Qwen/Qwen3.8-27B-FP8 tokenizer. Image tokens estimated as one per 28 x 28 pixel patch, as Qwen-VL models encode images; other models differ (Claude: about width x height / 750).

<details><summary>Ontario (MTO): per page</summary>

| Page | Words | Text tokens | Images | Image tokens |
|---|---:|---:|---:|---:|
| `index` | 382 | 482 | 0 | 0 |
| `getting-your-drivers-licence` | 4,619 | 6,088 | 10 | 174 |
| `safe-and-responsible-driving` | 466 | 554 | 0 | 0 |
| `getting-ready-drive` | 3,009 | 3,609 | 7 | 210 |
| `driving-along` | 976 | 1,156 | 2 | 178 |
| `sharing-road-other-road-users` | 2,661 | 3,259 | 10 | 1,432 |
| `driving-through-intersections` | 668 | 862 | 7 | 284 |
| `stopping` | 1,224 | 1,481 | 7 | 506 |
| `changing-directions` | 2,276 | 2,848 | 15 | 544 |
| `changing-positions` | 1,260 | 1,498 | 5 | 422 |
| `parking-along-roadways` | 1,674 | 2,020 | 4 | 326 |
| `freeway-driving` | 1,150 | 1,420 | 2 | 140 |
| `dealing-particular-situations` | 3,280 | 3,987 | 2 | 224 |
| `driving-night-and-bad-weather` | 2,401 | 2,935 | 2 | 150 |
| `dealing-emergencies` | 1,146 | 1,362 | 0 | 0 |
| `driving-efficiently` | 865 | 1,102 | 0 | 0 |
| `traffic-signs-and-lights` | 55 | 68 | 0 | 0 |
| `signs` | 2,280 | 2,831 | 112 | 2,136 |
| `traffic-lights` | 927 | 1,089 | 17 | 402 |
| `pedestrian-signals` | 289 | 347 | 2 | 60 |
| `pavement-markings` | 455 | 572 | 9 | 598 |
| `keeping-your-drivers-licence` | 2,061 | 2,667 | 1 | 98 |
| `other-ways-lose-your-licence` | 2,163 | 2,769 | 0 | 0 |
| `your-vehicle` | 64 | 76 | 0 | 0 |
| `maintaining-your-vehicle` | 787 | 1,003 | 2 | 204 |
| `vehicle-insurance-and-registration` | 455 | 575 | 0 | 0 |
| `towing` | 1,712 | 2,057 | 1 | 126 |
| `test-yourself-sample-knowledge-test-questions` | 370 | 526 | 0 | 0 |
| `level-two-road-test` | 5,874 | 7,058 | 11 | 414 |
| `off-road-vehicles-snowmobiles` | 8,240 | 10,391 | 17 | 682 |

</details>

<details><summary>California (DMV): per page</summary>

| Page | Words | Text tokens | Images | Image tokens |
|---|---:|---:|---:|---:|
| `index` | 276 | 349 | 2 | 98 |
| `dmv-services` | 97 | 205 | 0 | 0 |
| `copyright` | 84 | 121 | 0 | 0 |
| `disclaimer` | 43 | 65 | 0 | 0 |
| `the-california-driver-license` | 243 | 350 | 0 | 0 |
| `getting-an-instruction-permit-and-drivers-license` | 673 | 915 | 0 | 0 |
| `the-testing-process` | 839 | 1,095 | 0 | 0 |
| `changing-replacing-and-renewing-your-drivers-license` | 267 | 355 | 0 | 0 |
| `introduction-to-driving` | 858 | 1,124 | 3 | 48 |
| `navigating-the-roads` | 3,076 | 3,858 | 18 | 1,518 |
| `navigating-the-roads-cont1` | 1,731 | 2,103 | 8 | 767 |
| `laws-and-rules-of-the-road` | 1,740 | 2,256 | 26 | 1,499 |
| `laws-and-rules-of-the-road-cont1` | 2,761 | 3,526 | 11 | 1,586 |
| `laws-and-rules-of-the-road-cont2` | 1,412 | 1,782 | 0 | 0 |
| `safe-driving` | 2,176 | 2,777 | 2 | 234 |
| `safe-driving-cont1` | 744 | 897 | 1 | 144 |
| `safe-driving-cont2` | 1,235 | 1,595 | 1 | 252 |
| `alcohol-and-drugs` | 1,124 | 1,413 | 1 | 703 |
| `financial-responsibility-insurance-requirements-and-collisions` | 692 | 929 | 0 | 0 |
| `vehicle-registration-requirements` | 124 | 166 | 0 | 0 |
| `driver-safety` | 455 | 585 | 1 | 364 |
| `seniors-and-driving` | 547 | 742 | 0 | 0 |
| `glossary` | 266 | 355 | 0 | 0 |

</details>

<details><summary>Texas (DPS): per page</summary>

| Page | Words | Text tokens | Images | Image tokens |
|---|---:|---:|---:|---:|
| `index` | 1,273 | 2,006 | 3 | 2,695 |
| `chapter-1-your-license-to-drive` | 8,453 | 11,017 | 2 | 402 |
| `chapter-2-vehicle-inspection-and-registration` | 1,647 | 2,088 | 0 | 0 |
| `chapter-3-safety-responsibility` | 753 | 969 | 0 | 0 |
| `chapter-4-right-of-way` | 1,972 | 2,602 | 14 | 2,134 |
| `chapter-5-signals-signs-and-markers` | 4,213 | 5,182 | 147 | 3,728 |
| `chapter-6-signaling-passing-and-turning` | 1,346 | 1,616 | 8 | 625 |
| `chapter-7-parking-stopping-or-standing` | 1,081 | 1,287 | 7 | 1,276 |
| `chapter-8-speed-and-speed-limits` | 1,108 | 1,404 | 5 | 462 |
| `chapter-9-some-special-driving-situations` | 5,059 | 6,279 | 11 | 1,356 |
| `chapter-10-alcohol-and-drug-impact-on-the-driving-ability` | 2,954 | 4,091 | 0 | 0 |
| `chapter-11-motor-vehicle-crashes` | 1,372 | 1,737 | 0 | 0 |
| `chapter-12-pedestrian-safety` | 515 | 621 | 1 | 24 |
| `chapter-13-bicycle-laws-and-safety` | 758 | 951 | 1 | 42 |
| `chapter-14-additional-safety-tips` | 3,235 | 3,960 | 1 | 42 |
| `appendix-a-glossary-of-terms` | 3,261 | 3,909 | 0 | 0 |
| `appendix-b-driver-license-offices` | 197 | 260 | 0 | 0 |
| `appendix-c` | 1,373 | 2,077 | 0 | 0 |
| `appendix-d-fees` | 514 | 709 | 0 | 0 |
| `appendix-e-restriction-codes` | 569 | 950 | 0 | 0 |
| `back-cover` | 161 | 220 | 3 | 468 |

</details>

Regenerate with `python scripts/handbook_stats.py` (needs `beautifulsoup4` and `pillow`; `transformers` and the Qwen tokenizer for exact text tokens, otherwise 1.3 tokens per word).

What the numbers show:

- Each handbook fits in one long-context request: about 28k to 67k text tokens, and 7k to 13k more for the images.
- Text carries 79 to 88% of the tokens. The images are small (most are signs and diagrams under 250 px), but there are many of them, so dropping or keeping images changes a request by 12 to 21%.
- Most blocks are short (median 14 to 18 words), but 4 to 11% have more than 3 sentences, up to about 200 words. Citing such a block points to much more text than the rule came from, so sources need sentence-level ids.
- In the Ontario handbook, 87 of 245 images have alt text that names only the kind of sign ("a regulatory sign"). Without the image, a model has only the caption beside it.

## Repository layout

| Folder | What it holds |
|---|---|
| `handbooks/` | The three handbooks: `mto/` (Ontario), `ca/` (California), `tx/` (Texas). Each has its HTML pages, `images/` and the PDF in `source/` |
| `scrapers/` | The scripts that made `handbooks/` |
| `scripts/` | `handbook_stats.py`, which computes the analysis above |
| `docs/` | The prompts the team gave Claude (`prompt.md`) |

The earlier rule pipeline (rule language, census, rules database, extraction prompts and runs, the Qwen trial, review pages, and the first PDF-based Ontario rules) is kept on the branch [`archive/rule-pipeline`](https://github.com/hennyg888/Drive-Rule-Extraction-Bench/tree/archive/rule-pipeline).

## MTO Driver's Handbook – Offline Copy

A local, offline copy of [The Official MTO Driver's Handbook](https://www.ontario.ca/document/official-mto-drivers-handbook) from ontario.ca. Each page is saved as clean HTML, and every image is saved with it.

### Contents

```
scrapers/scrape_mto_handbook.py   # downloads the handbook
handbooks/mto/
├── index.html              # cover page (start here)
├── <chapter>.html          # one file per page, 29 in total (e.g. signs.html)
├── images/                 # all 241 images used in the content
├── source/MTO-drivers-handbook-ontario.ca.pdf   # the handbook as a PDF from ontario.ca
└── style.css               # shared stylesheet
```

### Usage

```sh
pip install requests beautifulsoup4
python scrapers/scrape_mto_handbook.py
```

Open `handbooks/mto/index.html` in a browser. Running the script again downloads every page again. Images already in `images/` are skipped.

### Differences from the online version

The handbook content matches the live site. Checked against ontario.ca on 2026-10-06: the text of all 30 pages is the same word for word, and all 241 images are byte-identical with the same alt text. The only differences are these deliberate changes:

**Added**
- A table-of-contents sidebar, previous/next buttons and an "On this page" list on every page.
- Anchor ids on section headings, so the "On this page" list can link to them.
- An Updated/Published dates line, and a "Source:" link to the page on ontario.ca.

**Removed**
- The site's header, footer, breadcrumbs, menus, scripts and tracking code.
- Inline `style` and `data-*` attributes.
- The site's empty "On this page" placeholder, which is filled in by JavaScript on the live site.

**Changed**
- **Links:** links between handbook pages point to the local `.html` files, including `#section` jumps. All other links stay as they are on the site, changed to full addresses.
- **Images:** image paths point to the local `images/` folder.
- **Formatting:** the HTML is indented so it's easy to read. Text inside paragraphs is kept on one line, so spacing doesn't change.

## California Driver's Handbook – Offline Copy

A local, offline copy of the [California Driver's Handbook](https://www.dmv.ca.gov/portal/handbook/california-driver-handbook/) from dmv.ca.gov, plus the DMV's PDF edition of the same handbook (DL 600, Rev. 6/2025). It is made the same way as the MTO copy and reuses its page template and stylesheet.

### Contents

```
scrapers/scrape_ca_handbook.py    # downloads the handbook and the PDF
handbooks/ca/
├── index.html              # cover page with the Secretary's message (start here)
├── <page>.html             # one file per web page, 22 in total (e.g. navigating-the-roads.html)
├── images/                 # all 74 images used in the content
├── source/DL-600.pdf       # the DMV's PDF edition, 92 pages
└── style.css               # the MTO stylesheet, plus nested "On this page" lists
```

The pages follow the site's own order: the front matter (DMV Services, Copyright, Disclaimer), then Sections 1 to 14. Long sections are split across several web pages on the site, and keep that split here: Section 6 is `navigating-the-roads.html` and `navigating-the-roads-cont1.html`, Section 7 is `laws-and-rules-of-the-road.html` plus `-cont1` and `-cont2`, and Section 8 is `safe-driving.html` plus `-cont1` and `-cont2`.

### Usage

```sh
pip install requests beautifulsoup4
python scrapers/scrape_ca_handbook.py
```

Open `handbooks/ca/index.html` in a browser. The script waits a second between requests. Running it again downloads every page again; the PDF is downloaded only if `source/DL-600.pdf` is missing.

### Differences from the online version

The handbook content matches the live site. Checked against dmv.ca.gov on 2026-10-20: the text of all 23 pages (21,413 words) is the same word for word, the headings match level for level, and all 74 images are byte-identical with the same alt text. None of the 955 links between the local files is broken. The web pages were last updated between November 2024 and September 2026, so in places they may differ from the June 2025 PDF; the two were not compared.

**Added**
- A table-of-contents sidebar, previous/next buttons and an "On this page" list on every page.
- An anchor id on every heading (h2 to h4), so citations can point to subsections.
- An Updated/Published/Retrieved dates line, from each page's metadata, and a "Source:" link to the page on dmv.ca.gov.

**Removed**
- The site's header, footer, breadcrumbs, menus, chat assistant, scripts and tracking code.
- Table labels that the site shows only on phones (they repeat the column headers), and empty spacer paragraphs.
- Two-column layout wrappers. Content keeps the site's source order, so an image may come just before the text it sits beside.
- Inline `style`, `class` and `data-*` attributes.

**Changed**
- **Links:** links between handbook pages point to the local `.html` files. All other links stay as they are on the site, changed to full addresses.
- **Images:** image paths point to the local `images/` folder.
- **Formatting:** the HTML is indented so it's easy to read. Text inside paragraphs is kept on one line. Non-breaking spaces became ordinary spaces.

Notes for readers: captions are the paragraph after their image, and some are a single word ("Right", "Wrong"). Nine images have no alt text on the site. The "DO NOT PASS" and "SLOWER TRAFFIC KEEP RIGHT" signs appear only inside the image `Sign-Sample-1.png`.

## Texas Driver Handbook – Offline Copy

A local copy of the [Texas Driver Handbook](https://www.dps.texas.gov/internetforms/Forms/DL-7.pdf) (DL-7, revised January 2026) from the Texas Department of Public Safety. Texas publishes the handbook only as a PDF, so the script downloads the PDF and converts it into the same kind of HTML pages as the other two handbooks.

### Contents

```
scrapers/scrape_tx_handbook.py    # downloads the PDF and converts it
handbooks/tx/
├── index.html              # cover, introduction, contact details, the Colonel's letter and the contents (start here)
├── chapter-<n>-<title>.html   # Chapters 1 to 14 (e.g. chapter-6-signaling-passing-and-turning.html)
├── appendix-<x>-<title>.html  # Appendices A to E
├── back-cover.html
├── images/                 # 203 images rendered from the PDF
├── source/DL-7.pdf         # the original PDF, 91 pages
└── style.css               # the MTO stylesheet, plus notes and captions
```

### Usage

```sh
pip install requests beautifulsoup4 pymupdf
python scrapers/scrape_tx_handbook.py   # add --verify to print the checks below
```

Open `handbooks/tx/index.html` in a browser. The PDF is downloaded only if `source/DL-7.pdf` is missing; the conversion runs every time.

### How the PDF was converted

- **Reading order and headings** come from the PDF's own tags (it is a tagged PDF with no bookmarks). Paragraphs and lists that continue across a page break are joined, and words hyphenated at line ends are rejoined.
- **Running headers, footers and page numbers** are left out, as are table headers and "(Continued)" titles that the PDF repeats on every page of a long table.
- **Page references:** every paragraph, list item, heading and table row carries `data-pdf-page` (the PDF page) and `data-page-label` (the page number printed on it). Each page's "Source:" link opens the PDF at its first page.
- **Images:** the 203 images are rendered from the PDF: 84 figures and 119 sign, shape and colour cells from the sign tables. The PDF has no alt text, so each image's alt text comes from its caption (134), from text next to it (41), or was written by hand from the picture (28, mostly signs whose lettering is drawn as shapes). The `data-alt-source` attribute on each image says which.
- **Sign tables** (Tables 16 to 21) are two-column Sign | Description tables, one sign per row, with each table's title as its caption.
- **Special Notes** are paragraphs with class `note`, placed after the paragraph or list they sit beside in the PDF.
- **Text is kept as printed**, including its typos.

### Checks

Checked on 2026-10-20 with `--verify`:

- **Text:** the HTML holds 98.2% of the PDF's words (99.8% counting list numbers, which the browser draws, and alt text). What is left out is the chapter titles, which are in each page's `<h1>` rather than its text, and the repeated table headers. No run of four or more words from the PDF is missing on any page, and the HTML adds no words.
- **Order:** every one of the 1,557 text blocks starts with words found on the PDF page it names. Page breaks, two-column pages and figures with text wrapped around them were spot-checked by hand.
- **Images:** all 203 images referenced by the pages exist, and each of the 119 sign images was checked against its description.
