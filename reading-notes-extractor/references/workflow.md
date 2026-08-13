# Workflow — full procedure

This file expands the five steps in SKILL.md. Read it when handling your first batch in a session.

## Contents

1. Parse the table of contents
2. Identify page numbers and locate chapter
3. Extract marked text and visual objects
4. Handle cross-page fragments and splicing
5. Produce output

## Step 1 — Parse the table of contents

Triggered only when the user uploads a TOC (目录/目次) image.

1. Recognize every title, its hierarchy level (part / chapter / section), and its starting page number.
2. Preserve the original title text — do not reword.
3. Generate a Markdown outline reflecting the hierarchy.
4. Infer page ranges:
   - chapter start = listed page number;
   - chapter end = (next same-or-higher-level title's start page) − 1;
   - if the end can't be determined, mark "起始页以后，待后续目录确认".
5. Output: (a) the recognized outline, (b) page range per chapter, (c) a separate "待确认项" list for any uncertain titles or page numbers.

Outline format example:

```
# 书名或读书笔记标题

## 第一章 章节名称（第1-20页）

### 第一节 小节名称（第3-8页）

### 第二节 小节名称（第9-20页）
```

Notes on common TOC photo issues: page curvature and shooting angle can misalign labels (e.g. 附录A/附录B) with their titles vertically. Reconcile against the book's actual structure and state the assumption in the recognition notes, inviting correction.

**Lock the page ranges as authoritative state once derived.** Do not silently re-infer them on later batches — chapter boundaries must not drift between batches. Revise only on a corrected TOC or explicit user request.

## Step 2 — Identify page numbers and locate chapter

For every body-page batch:

1. Look for page numbers at edges, headers, footers, and corners first. **Uploaded photos may be out of order** — always read the real page number first and process/sort by it, not by upload position.
2. Page numbers may be Arabic, Roman, Chinese, or small print.
3. If an image contains both a left and a right page, recognize and process each page's number separately.
4. Compare each page's recognized number to the locked TOC ranges to locate the most specific chapter or section.
5. **File strictly by page number.** An extraction belongs to the chapter whose locked range contains its own page number — never to a chapter just because a neighboring page in the same photo belonged there. If one page spans two chapters, split content into the respective chapters based on titles, page-number position, and body content.
6. **Conflict check:** if an extraction's page number falls outside the range of the chapter you're about to file it under, re-read the page number; if it still conflicts, file by the page number (ranges are authoritative) and flag it in the recognition notes. Do not force a page into a chapter whose range doesn't contain it.
7. If a page number is unreadable: try inferring from running heads, chapter titles, and context; if still unknown, file under "待确认章节".

## Step 3 — Extract marked text and visual objects

Mark types include but are not limited to:
1. text wrapped by a hand-drawn bracket: `【】`, `[]`, `〔〕`, `()`, `（）`;
2. text with underlines, wavy lines, or double lines beneath it;
3. text covered by highlighter, color block, or fluorescent pen;
4. paragraphs with a side vertical bar, brace, circle, or arrow in the margin;
5. body text a hand-drawn symbol clearly points to;
6. a visual object selected by a nearby/touching star, arrow, check mark, circle, bracket, side-bar, or other object-level symbol;
7. every visual object on supplied photos when an explicit or session-persistent all-visuals scope is active.

**Annotation bracket vs. printed parenthesis (critical — most common manual fix):**
- A reader's *hand-drawn bracket* around a passage is a MARK. Output the enclosed text WITHOUT the bracket symbols — the bracket never appears in your output.
- A *printed parenthesis* that is part of the typeset text (a short inline gloss / transliteration / citation / aside, e.g. `（Iwan）`, `（heuristics）`, `（约50万人）`) is CONTENT. Keep it exactly.
- Telling them apart: hand-drawn marks are large, irregular, wrap a whole clause/sentence/paragraph, often touch line edges; printed parentheses are small, regular, typeset, sit inside a sentence around a brief gloss. When a bracket clearly wraps a whole marked passage, strip it.

Extraction rules (verbatim, plain text):
1. Keep the original text — no summarizing, rewriting, or polishing — and add NO bold/italics/emphasis of your own. Output is plain text; the only added marks are the page-number superscript and the uncertainty notations.
2. Preserve original punctuation, proper nouns, numerals, and English capitalization during OCR.
3. A mark covering a full sentence → extract the full sentence.
4. A mark spanning multiple lines but semantically continuous → merge into one quotation.
5. A side-bar covering one or more paragraphs → extract the full corresponding paragraph(s).
6. **Partial mark → snap to sentence boundary.** Prefer extracting the full sentence the marked span belongs to rather than a dangling fragment. Do not emit half-sentences or `……（碎片）` shards stitched with ellipses. If the marked span is genuinely a clean sub-clause, extract that sub-clause as a readable unit (minimal punctuation may be added); never leave a piece broken mid-phrase.
7. Don't extract unmarked ordinary body text.
8. Don't mistake running heads, footers, footnote numbers, or page numbers for marks.
9. After applying any explicit all-visuals request, a page with no selected text or visual → return only: `该页未发现标注内容。` (or source-language equivalent).

### Visual objects

When a mark unambiguously selects a table, matrix, chart, diagram, map, timeline, screenshot, illustration, or other visual, extract the entire object rather than only the labels closest to the mark. Strip the reader's selection symbol. An explicit all-visuals request selects every visual on each supplied photo, including multiple objects on one page. If the user states that every uploaded photo contains a visual to extract, keep that rule active for the current book session.

Build one visual semantic unit from:

- the core visual and its explicit structure;
- figure/table number, title/caption, legend, axes, units, source, visual-specific footnotes, and printed callouts;
- only the minimum nearby sentence(s) that directly introduce or decode the visual, placed under `Associated explanation:`.

Do not include ordinary nearby prose merely because it is close. A run of paragraphs that defines the visual's terms or continues the author's argument is ordinary exposition, even though it is topically related; include it only when independently marked. When independently marked prose follows the visual block, place `Other independently marked text:` before it so it cannot be mistaken for associated explanation. Read `visual-extraction.md` for representation routing, text-first degradation, fidelity rules, and the three quality gates. Read `svg-reconstruction.md` before producing fenced SVG.

## Step 4 — Cross-page fragments and splicing

A mark or selected visual may be cut off at a page boundary. Common cases:
1. page opens with only a closing symbol `]` `】` `)` `）`;
2. page ends with only an opening symbol `[` `【` `(` `（`;
3. an underline / highlight / vertical bar continues from the previous page to the next;
4. a sentence breaks at page end and continues on the next page;
5. one marked passage is split by pagination;
6. a table, diagram, legend, caption, or other visual unit continues on an adjoining page.

Handling rules:
1. If the current page's opening clearly continues an unfinished mark from the previous page, merge it with the held fragment.
2. If the current page ends with an unfinished mark, hold it as a "待拼接片段" and wait for the next page.
3. If you must output immediately, mark it:
   ```
   > [待续] 当前页识别到的残缺标注文本……
   ```
4. Once the next page completes it, output the merged full content and note:
   ```
   已与上一页残缺标注合并。
   ```
5. Splicing only restores continuity of the original — never expand or invent text, cells, lines, arrows, labels, or data.
6. If you can't tell how to splice, keep it as-is and mark:
   ```
   > [疑似残缺，待确认] ……
   ```
7. **Never silently emit a truncated extraction.** A blockquote that stops mid-sentence with no `[页底截断]` / `[待续]` marker is a bug. Mark every truncation the same way, every time.
8. Hold a cross-page visual until all parts arrive. If immediate output is required, mark it `[visual partially clipped; continuation pending]` and report which side is missing.

**Coverage check before finishing a batch** (guards against whole-object omissions):
- every page number identified in this batch is accounted for (produced extractions, or noted as having none);
- every opening bracket / underline / side-bar that left the bottom edge has a matching pending fragment;
- every object-level mark has a target, and every selected visual has its required attachments or a stated reason they are missing;
- every clipped or cross-page visual has a matching pending record;
- no page in a continuous run was skipped; if covered page numbers have a gap, report it in the recognition notes.

## Step 5 — Output (see also output-templates.md)

Per-batch default: output only this batch's new extractions, grouped by chapter, each blockquote ending with a superscript page number, as plain text (no bold/emphasis).

For selected visuals, output a figure/table heading plus the least-lossy structured representation. Default to a single Markdown file containing structured transcription and, when justified, SVG in an Obsidian SVG Editor-compatible `svg` fence—no screenshots, image links, or Base64. Use the required fixed canvas and explicit foreground palette. Save and embed one crop only in an explicitly requested evidence mode. Put direct associated explanation under a separate label. Use the exact visual templates in `output-templates.md`; do not output placeholder image links.

**Order by page number ascending within each chapter**, even when photos arrived out of order; order chapters by the TOC.

Multiple chapters in one batch → output under separate chapter headings in TOC order.

Uncertain page/chapter:
```
### 待确认章节（疑似第X页）

> [章节待确认] 标注内容……
```

Uncertain word in OCR:
```
> 原文前半部分〔疑似：某词〕原文后半部分。
```

Do not explain the marked content in your own words. Neutral structural labels are allowed for visual transcription; interpretation is not. Use recognition notes only to clarify page/chapter/OCR/visual uncertainty. Before delivery, validate visual-heavy Markdown with `scripts/validate_visual_markdown.py`, then check SVG Editor rendering in Obsidian Live Preview and Reading View and visually compare it with the source.
