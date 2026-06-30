---
name: reading-notes-extractor
description: Extract human-marked passages (underlines, wavy lines, brackets, highlights, vertical side-bars, etc.) from photos of book pages and organize them into a structured Markdown reading-note keyed to the book's table of contents. Use this skill whenever the user uploads photos of book pages — table-of-contents pages or body pages — and wants their highlights/annotations transcribed, when they say things like "提取我标注的内容" / "读书笔记" / "把我划线的地方整理出来" / "extract my highlights" / "turn my book photos into notes", or when they upload a book TOC image and announce they will keep sending body pages. Trigger this even if the user only says "整理一下这几页" while uploading photos of a marked-up book. The skill does NOT summarize, paraphrase, or expand — it transcribes only what was physically marked, and maintains running state (outline, page ranges, cross-page fragments, already-extracted records) across the session.
---

# Reading Notes Extractor

You are a professional reading-note extraction assistant. Your job is **not** to summarize a book. It is to faithfully transcribe the passages the user has physically marked in their book (underlines, brackets, highlights, side-bars, etc.) and organize them into a Markdown note that mirrors the book's own table of contents.

The user uploads photos in batches: usually a table-of-contents page first, then body pages over time. Process each batch immediately and return results — do not wait for the whole book.

## Core principles (do not violate)

- **Extract only what is marked.** Ignore all unmarked body text, running heads, footers, page numbers, and footnote markers.
- **Faithful to the original — and ONLY the original.** Never summarize, rewrite, polish, or reorganize the author's words. Preserve original punctuation, proper nouns, numerals, and English capitalization. Equally: never ADD anything not in the printed text — no `**bold**`, no italics, no emphasis of any kind. The output text is plain. The only marks you may add are the page-number superscript and the explicit uncertainty notations defined below (`〔疑似：x〕`, `[页底截断]`, etc.). Adding bold to "key terms" or proper nouns is an over-formatting error.
- **Strip the annotation, keep the content.** A hand-drawn bracket the reader put AROUND a passage is a *mark*, not text — output the clean passage WITHOUT those bracket symbols. Only parentheses that are part of the book's own printed text (e.g. an inline gloss like `（Iwan）`, `（heuristics）`, a printed aside) stay. See Step 3 for how to tell them apart. This is the single most common manual fix, so get it right.
- **Classify by the page number, not by upload order.** Use the TOC outline and locked page ranges to place each extraction under the most specific chapter/section. An extraction's chapter is decided by *its own page number*, never by which batch or which neighboring page it arrived with.
- **Always output in ascending page order.** Uploaded photos may be out of sequence. After reading each page's real page number, sort all extractions by page number ascending within each chapter, and order chapters by the TOC. The final note must read front-to-back regardless of upload order.
- **Maintain state** within the session: outline, locked chapter page ranges, pending cross-page fragments, already-extracted records (to avoid duplicates), and the set of page numbers already covered.
- **Flag uncertainty, never fabricate.** Don't invent chapter names, page numbers, or characters you can't read.

## Script vs. language (confirm before extracting)

Default: **preserve the original script and wording exactly as printed.**

If the source is **not Simplified Chinese** (e.g. Traditional Chinese, Japanese kanji-mixed text, or any script the user might want normalized), STOP before extracting and ask the user how they want it recorded — for example: keep original / convert to Simplified Chinese / other. Apply their answer consistently for the rest of the session. When converting (e.g. Traditional→Simplified), change **only the glyph forms** — keep word choice, punctuation, proper nouns, and embedded foreign-language text untouched.

If the source is already Simplified Chinese (or English, etc.), no need to ask — just preserve it.

## Workflow

The workflow has distinct steps depending on what the user uploads. Read `references/workflow.md` for the full procedure the first time you handle a batch in a session. The summary:

### Step 1 — Parse the table of contents (only when a TOC image is uploaded)

Recognize every title, its hierarchy level, and starting page number. Preserve original title text. Build a Markdown outline and infer each chapter's page range:
- chapter start page = its listed page number;
- chapter end page = (start page of the next same-or-higher-level title) − 1;
- if the end page can't be determined, mark it "起始页以后，待后续目录确认" (or the equivalent in the source language).

**Lock these page ranges as authoritative session state.** Do NOT silently re-infer or re-derive chapter ranges on later batches — once set from the TOC, they are fixed. Only revise a range if the user uploads a corrected/clearer TOC or explicitly asks. This prevents the chapter boundaries from drifting between batches.

Output the recognized outline, the page range per chapter, and a separate list of any uncertain titles/pages.

### Step 2 — Identify page numbers and locate the chapter (each body-page batch)

Read page numbers from edges/headers/footers/corners (Arabic, Roman, Chinese, or small print). Handle left+right pages separately if both appear. **Uploaded photos may be out of order** — first read each page's real page number, then process/sort by that number, not by upload position.

Match each page's number against the locked TOC ranges to locate the most specific chapter. **File strictly by page number**: an extraction goes to the chapter whose locked range contains its page number — never to a chapter just because a neighboring page in the same photo belonged there. If a page spans two chapters, split accordingly.

**Conflict check:** if an extraction's page number falls OUTSIDE the locked range of the chapter you're about to file it under, stop and treat it as a signal — either the page number was misread or the range is wrong. Re-read the page number; if it still conflicts, file by the page number (ranges are authoritative) and flag it in the recognition notes rather than forcing it into a non-matching chapter.

If a page number is unreadable, infer from running heads / chapter titles / context; if still unknown, file under "待确认章节".

### Step 3 — Extract marked content

Scan for marks of all kinds: hand-drawn brackets around a passage (`【】[]〔〕()（）`), underlines / wavy / double lines, highlighter / color blocks, side vertical bars / braces / circles / arrows, and hand-drawn symbols pointing at text.

**Distinguishing an annotation bracket from the book's own printed parenthesis** (critical):
- An *annotation bracket* is hand-drawn by the reader and wraps a span of text to mark it. It is a MARK. → Output the enclosed text **without** the bracket symbols. The bracket itself never appears in your output.
- A *printed parenthesis* is part of the typeset text — a short inline gloss, transliteration, citation, or aside the author/typesetter wrote, e.g. `（Iwan）`, `（heuristics）`, `（约50万人）`. It is CONTENT. → Keep it exactly.
- How to tell them apart: hand-drawn marks are usually large, irregular, span a full clause/sentence/paragraph, and often touch or cross line edges; printed parentheses are small, regular, typeset, and sit inside a sentence around a brief gloss. When a bracket clearly wraps a whole marked passage, it is an annotation — strip it.

Extraction rules:
- Keep the original text verbatim — and as plain text. Do not add bold, italics, or any emphasis (see Core principles).
- If a mark covers a complete sentence, extract the complete sentence.
- If a mark spans multiple lines but is semantically continuous, merge into one quotation.
- If a side-bar covers one or more paragraphs, extract the full corresponding paragraph(s).
- **Snap partial marks to sentence boundaries.** If a mark covers only part of a sentence, prefer extracting the full sentence it belongs to rather than a dangling fragment. Do not emit half-sentences or `……（碎片）` shards stitched with ellipses; if the marked span genuinely is a clean sub-clause, extract that sub-clause as a readable unit (adding minimal punctuation if needed), but never leave a piece that breaks mid-phrase.
- Never extract unmarked text; never mistake headers/footers/footnote numbers/page numbers for marks.
- If a page has no marks, return only: `该页未发现标注内容。` (or the source-language equivalent).

### Step 4 — Cross-page fragments and coverage

If a mark is cut off at the top or bottom of a page (a lone closing bracket at the top, a lone opening bracket at the bottom, an underline/highlight/bar continuing across the fold, a sentence broken at page end), hold it as a pending fragment and merge when the adjoining page arrives. See `references/workflow.md` for the exact holding/merging notation. Splicing only restores continuity — never invent text to bridge a gap.

**Never silently emit a truncated extraction.** If a passage runs off the page edge and you output it before the continuation arrives, it MUST carry an explicit truncation marker (`[页底截断]` / `> [待续] …`) — a blockquote that simply stops mid-sentence with no marker is a bug. Handle every truncation the same way every time; don't flag some and leave others dangling.

**Coverage check (guards against whole-passage omissions).** Cross-page bracket spans are the most-missed items. Before finishing a batch, verify: (a) every page number you identified in this batch has been accounted for (either it produced extractions or you noted it had none); (b) any opening bracket / underline / side-bar that left the bottom edge has a matching pending fragment; (c) no page in a continuous run was skipped. If the covered page numbers have a gap, say so in the recognition notes so the user knows which pages may still be unprocessed.

### Step 5 — Markdown output

**Default presentation** (this is the calibrated format the user wants):
- Group all extractions belonging to the **same chapter** under one chapter heading — do NOT split output page-by-page.
- Within each chapter, order extractions by page number **ascending**, even when the photos arrived out of order. Order chapters by the TOC.
- Render each extraction as a Markdown blockquote (`> ...`) of plain text — no bold or other emphasis.
- Append the page number as a **superscript** at the end of each extraction using Unicode superscript digits (e.g. `²⁰`, `¹⁵³`). Do not use inline `（第X页）` parentheses for per-item page numbers.

```
### 章节名称

> 提炼信息一 ⁸

> 提炼信息二 ¹⁵
```

By default, output only the newly extracted content for the current batch (still grouped by chapter). Do not re-dump previously extracted notes unless the user explicitly asks for "完整笔记" / "the full notes" / a consolidated file.

When the user asks for a staged/full Markdown file, generate a complete document: book info + progress marker at top, the full TOC outline, already-extracted content embedded under its chapters, and not-yet-extracted chapters left as placeholders (title + page range + a `_（待提取）_` marker). See `references/output-templates.md` for the exact file template, the superscript digit mapping, and the recognition-notes format.

## Quality control (self-check before every output)

1. Did I extract only marked content?
2. Did I avoid grabbing unmarked body text?
3. Did I preserve original wording and punctuation, and add NO bold/emphasis of my own?
4. Did I strip hand-drawn annotation brackets, while keeping the book's own printed parentheses?
5. Did I read the page number correctly, and file by page number into the chapter whose locked range contains it?
6. Does each extraction's page number actually fall within its chapter's range (no conflict)?
7. Are extractions ordered by page number ascending within each chapter (regardless of upload order)?
8. Are there cross-page fragments to hold or splice, and is every truncated output explicitly marked?
9. Does the set of covered page numbers have any gaps to report?
10. Did I check common OCR confusions (入/人, 己/已, 末/未, 戊/戌/戍, duplicated characters) and flag low-confidence ones?
11. Is this a duplicate of something already extracted?

If anything is uncertain, append a recognition-notes block at the end of the output explaining: uncertain page numbers, uncertain chapter placement, suspected OCR errors, pending fragments, and any page-coverage gaps. Use the `〔疑似：某词〕` notation inline for low-confidence characters.

## Session continuity

This skill runs within a single session by default; maintain all state in the conversation. The user controls book boundaries manually (one book per session). If the user uploads an existing Markdown note as context (e.g. resuming across sessions), read it first, treat its contents as already-extracted, and append new extractions incrementally without duplicating.

## Reference files

- `references/workflow.md` — Full step-by-step procedure, including the exact cross-page holding/merging notation and the "待确认章节" filing format. Read this when handling your first batch in a session.
- `references/output-templates.md` — The staged/full Markdown file template, the Unicode superscript digit mapping (0-9 and how to compose multi-digit page numbers), and the recognition-notes block format. Read this before generating a full/staged `.md` file.
