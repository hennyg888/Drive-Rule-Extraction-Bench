# Drive-Rule-Extract-Bench

This is a dataset and framework for benchmarking how well visual language models (VLMs) can extract formalized rules of the road from a driver's handbook. It tests for accuracy, coverage, and correct attribution to source materials as input modalities vary (E.g. text-only, text-and-image, whole page as image). 

Project for VLM CS886 F26 by Michael Lee and Henry Guo.

## Handbooks

Three handbooks, each kept two ways: a human-readable PDF, and a parsed set of local HTML pages and images that LLMs can read. The HTML copies are the source text given to the models.

| Handbook | PDF | Parsed HTML and images | Made by |
|---|---|---|---|
| Official MTO Driver's Handbook (Ontario) | `handbooks/mto/source/MTO-drivers-handbook-ontario.ca.pdf` | `handbooks/mto/`: 30 pages, 241 images | `scrapers/scrape_mto_handbook.py` (from ontario.ca web pages) |
| California Driver's Handbook, DL 600 (Rev. 6/2025) | `handbooks/ca/source/DL-600.pdf` | `handbooks/ca/`: 23 pages, 74 images | `scrapers/scrape_ca_handbook.py` (from dmv.ca.gov web pages) |
| Texas Driver Handbook, DL-7 (revised January 2026) | `handbooks/tx/source/DL-7.pdf` | `handbooks/tx/`: 21 pages, 203 images | `scrapers/scrape_tx_handbook.py` (from the DPS PDF; Texas publishes no web version) |

The handbooks are state- and province-wide: San Francisco and Austin drivers use the California and Texas handbooks.

All three HTML copies have the same layout, so one program can read any of them. The handbook text is inside `<article class="content">`, with headings, lists and tables as ordinary HTML and every image in the folder's `images/`. Open `index.html` in each folder to browse it.

## Repository layout

| Folder | What it holds |
|---|---|
| `handbooks/` | The three handbooks: `mto/` (Ontario), `ca/` (California), `tx/` (Texas). Each has its HTML pages, `images/` and the PDF in `source/` |
| `scrapers/` | The scripts that made `handbooks/` |
| `analysis/` | Rule language v1, the Ontario census, the passing rules for each handbook (`analysis/passing-rules/`), handbook passages (`analysis/segments/`) and notes on using the rules in a VLA |
| `prompts/` | Extraction prompts and their parts: the fixed prompt (`extract-rules.fixed-v1.md`), the principle-based variant (`extract-rules.md`), topics, worked examples and passage selection |
| `tools/` | Splitting handbooks into passages, making passage files, checking statements, building the review pages |
| `qwen/` | Running the extraction on open models with vLLM, and scoring it against the reference |
| `pages/` | Review pages: rules side by side with the handbook text |
| `pipeline/`, `provenance/` | How the rule set is made, step by step, and how the Ontario reference was made |
| `extractions/`, `runs/` | Model outputs |
| `docs/` | The prompts the team gave Claude (`prompt.md`) and other write-ups |
| `legacy/` | The first Ontario passing rules, extracted from the PDF before the rule language existed |

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
