# Workflow — full procedure

This file expands the five steps in SKILL.md. Read it when handling your first batch in a session.

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

## Step 2 — Identify page numbers and locate chapter

For every body-page batch:

1. Look for page numbers at edges, headers, footers, and corners first.
2. Page numbers may be Arabic, Roman, Chinese, or small print.
3. If an image contains both a left and a right page, recognize and process each page's number separately.
4. Compare recognized page numbers to the TOC ranges to locate the most specific chapter or section.
5. If one page spans two chapters, classify content into the respective chapters based on titles, page-number position, and body content.
6. If a page number is unreadable: try inferring from running heads, chapter titles, and context; if still unknown, file under "待确认章节".

## Step 3 — Extract marked content

Mark types include but are not limited to:
1. text enclosed by bracket symbols: `【】`, `[]`, `〔〕`;
2. text in parentheses `()`, `（）` that is clearly a reading annotation (not the author's own parenthetical — use judgment from context);
3. text with underlines, wavy lines, or double lines beneath it;
4. text covered by highlighter, color block, or fluorescent pen;
5. paragraphs with a side vertical bar, brace, circle, or arrow in the margin;
6. body text a hand-drawn symbol clearly points to.

Extraction rules (verbatim):
1. Keep the original text — no summarizing, rewriting, or polishing.
2. Preserve original punctuation, proper nouns, numerals, and English capitalization during OCR.
3. A mark covering a full sentence → extract the full sentence.
4. A mark spanning multiple lines but semantically continuous → merge into one quotation.
5. A side-bar covering one or more paragraphs → extract the full corresponding paragraph(s).
6. Only part of a sentence marked → extract only the marked part; minimal punctuation may be added for readability.
7. Don't extract unmarked ordinary body text.
8. Don't mistake running heads, footers, footnote numbers, or page numbers for marks.
9. A page with no marks → return only: `该页未发现标注内容。` (or source-language equivalent).

## Step 4 — Cross-page fragments and splicing

A mark may be cut off at a page boundary. Common cases:
1. page opens with only a closing symbol `]` `】` `)` `）`;
2. page ends with only an opening symbol `[` `【` `(` `（`;
3. an underline / highlight / vertical bar continues from the previous page to the next;
4. a sentence breaks at page end and continues on the next page;
5. one marked passage is split by pagination.

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
5. Splicing only restores continuity of the original — never expand or invent text.
6. If you can't tell how to splice, keep it as-is and mark:
   ```
   > [疑似残缺，待确认] ……
   ```

## Step 5 — Output (see also output-templates.md)

Per-batch default: output only this batch's new extractions, grouped by chapter, each blockquote ending with a superscript page number.

Multiple chapters in one batch → output under separate chapter headings in order.

Uncertain page/chapter:
```
### 待确认章节（疑似第X页）

> [章节待确认] 标注内容……
```

Uncertain word in OCR:
```
> 原文前半部分〔疑似：某词〕原文后半部分。
```

Do not explain the marked content in your own words, except inside a recognition-notes block to clarify page/chapter/OCR uncertainty.
