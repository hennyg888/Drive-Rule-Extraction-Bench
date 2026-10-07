# Drive-Rule-Extract-Bench

This is a dataset and framework for benchmarking how well visual language models (VLMs) can extract formalized rules of the road from a driver's handbook. It tests for accuracy, coverage, and correct attribution to source materials as input modalities vary (E.g. text-only, text-and-image, whole page as image). 

Project for VLM CS886 F26 by Michael Lee and Henry Guo.

## MTO Driver's Handbook – Offline Copy

A local, offline copy of [The Official MTO Driver's Handbook](https://www.ontario.ca/document/official-mto-drivers-handbook) from ontario.ca. Each page is saved as clean HTML, and every image is saved with it.

### Contents

```
scrape_mto_handbook.py      # downloads the handbook
mto_drivers_handbook/
├── index.html              # cover page (start here)
├── <chapter>.html          # one file per page, 29 in total (e.g. signs.html)
├── images/                 # all 241 images used in the content
└── style.css               # shared stylesheet
```

### Usage

```sh
pip install requests beautifulsoup4
python scrape_mto_handbook.py
```

Open `mto_drivers_handbook/index.html` in a browser. Running the script again downloads every page again. Images already in `images/` are skipped.

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
