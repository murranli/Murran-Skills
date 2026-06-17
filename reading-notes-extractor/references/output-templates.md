# Output templates

Read this before generating a full/staged Markdown file, or whenever you need the superscript page-number mapping.

## Unicode superscript digits

Map each digit, then concatenate for multi-digit page numbers. There is no space between the text and the superscript except a single normal space before it.

| digit | superscript |
|-------|-------------|
| 0 | ⁰ |
| 1 | ¹ |
| 2 | ² |
| 3 | ³ |
| 4 | ⁴ |
| 5 | ⁵ |
| 6 | ⁶ |
| 7 | ⁷ |
| 8 | ⁸ |
| 9 | ⁹ |

Examples: page 8 → ` ⁸`; page 15 → ` ¹⁵`; page 153 → ` ¹⁵³`; page 487 → ` ⁴⁸⁷`.

Blockquote with page number:
```
> 这是一条被标注的原文。 ¹⁵
```

## Per-batch incremental output (default)

Group by chapter; output only the current batch's new extractions:

```
### 章节名称

> 提炼信息一 ⁸

> 提炼信息二 ⁸

### 另一章节名称

> 提炼信息三 ⁹
```

## Staged / full Markdown file

Generate this only when the user asks for "完整笔记" / a staged file / a consolidated `.md`. Structure:

```
# 《书名》读书笔记

> 作者：…｜原书名：…
> 说明：本笔记仅提取书中人工标注（下划线、波浪线、括号、竖线、高亮等）的原文，按原书目录章节归类，不做总结或改写。每条信息末尾上标数字为所在页码。
>
> **提取进度：……（已提取至第 N 页）**

---

## 前置内容

### 序　标题／作者（第7-10页）

> 已提取内容…… ⁷

### 导读　标题／作者（第11-18页）

> 已提取内容…… ¹¹

### 前言（第19-36页）

> 已提取内容…… ²⁰

---

## 第一部　部名（第37-152页）

### 1　章节名称（第37-52页）

_（待提取）_

### 2　章节名称（第53-62页）

> 已提取内容…… ⁵⁵

…（其余章节同理：已提取的嵌入内容，未提取的留 `_（待提取）_` 占位）…

---

## 附录

### 附录 A　标题（第539-555页）

_（待提取）_
```

Rules for the staged file:
- Keep the **complete TOC outline** — every chapter from Step 1, with its page range in the heading.
- Chapters with extractions: embed the blockquotes (with superscript page numbers) under their heading.
- Chapters without extractions yet: leave the heading plus `_（待提取）_`.
- Update the progress marker at the top to reflect how far extraction has reached.
- Save the file to the outputs directory and present it to the user. Suggest a filename like `《书名》_读书笔记.md`.

## Recognition-notes block

Append at the end of an output (per-batch or file) only when something is uncertain. Keep it factual — this is the one place you may speak in your own words, strictly to flag uncertainty:

```
识别说明：
- 页码识别不确定：……
- 章节归属不确定：……
- OCR 疑似错误：……
- 存在待拼接片段：……
```

Adapt the language of headings/labels to the user's working language when appropriate, but keep extracted passages in the agreed source-text form.
