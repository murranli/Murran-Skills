# Output templates

Read this before generating a full/staged Markdown file or a visual-object block.

## 1. Unicode superscript pages

| digit | superscript |
|---|---|
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

Concatenate digits: page 8 → ` ⁸`; page 15 → ` ¹⁵`; page 153 → ` ¹⁵³`.

## 2. Per-batch output

Group new extractions by chapter, in page order. Keep marked prose as plain blockquotes:

```markdown
### 章节名称

> 被标注原文。 ⁸

> 另一条被标注原文。 ¹⁵
```

## 3. Visual-object blocks

Use a level-four heading. Default to a single Markdown file with no image link. Self-contained Markdown may contain inline HTML tables when verified merged cells require them; it must not depend on sibling assets. Keep blank lines around every table, and keep Markdown header/separator/data rows contiguous.

### Simple matrix

```markdown
#### 图1-2　产品模型的检验矩阵 ⁷

结构化转录：

| 检验层次 | 维度一 | 维度二 | 维度三 |
|---|---|---|---|
| 是否能够 | 提高或不降低效率 | 降低或不提升成本 | 提升或不破坏体验 |
| 是否合理 | 提供的可能 | 发生的场景 | 接受的意愿 |
| 是否存在 | 市场 | 需求 | 用户 |

关联说明：

> 首先从最底层看要判断市场、需求，以及用户是否真正存在。 ⁷
```

Markdown table rules:

- Leave one blank line before the header and after the last data row.
- Do not insert blank lines between header, separator, and data rows.
- Do not put a table inside a blockquote.
- Escape a literal pipe as `\|`.
- Keep every row's column count equal.
- Use HTML or nested transcription when merged-cell structure is uncertain.

### SVG diagram or chart (Obsidian SVG Editor)

````markdown
#### 图X-X　原图标题 ²⁴

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 500" width="100%" role="img" aria-labelledby="fig-title fig-desc">
  <title id="fig-title">原图标题</title>
  <desc id="fig-desc">图中结构的简洁说明。</desc>
  <rect data-role="canvas-background" x="0" y="0" width="800" height="500" fill="#F5F7FA" fill-opacity="1" stroke="#000000" stroke-opacity="0.08" stroke-width="1"/>
  ...
</svg>
```

结构化转录：

- 节点：……
- 连接：……
- 层级/相对位置：……

关联说明：

> 与图表直接相关的原文。 ²⁴
````

Read `svg-reconstruction.md` before filling the SVG. Keep the `svg` fence unindented and outside blockquotes/lists/HTML wrappers. A statistical SVG with exact printed values must be followed by a compact data table as well as any axis/legend transcription.

### Text-only degradation

```markdown
#### 图X-X　原图标题 ²⁴

结构化转录：

- 可辨认对象：……
- 明确关系：……
- 〔关系待确认〕：……

识别说明：照片不足以可靠还原其余形态，因此未生成 SVG。
```

Use this when boundaries, merged cells, endpoints, or topology are uncertain. A restrained transcription is preferable to a plausible but incorrect drawing.

Use `其他独立标注：` only when independently marked prose follows the visual block. If a sentence is both independently marked and direct associated explanation, include it only once under `关联说明：`.

### Optional evidence mode

Only when the user explicitly requests visual evidence, add one real saved crop after the heading:

```markdown
![图1-2 产品模型的检验矩阵](figures/p007-fig1-2.png)
```

Never emit a placeholder or Base64 image. Keep one final crop per object, use a stable relative path, and apply only non-generative readability corrections.

## 4. Staged/full Markdown file

Generate only when the user requests a complete, staged, or consolidated note:

```markdown
# 《书名》读书笔记

> 作者：…｜原书名：…
> 说明：本笔记提取书中人工标注的原文与被选可视化对象，按原书目录归类，不做总结或改写。图表以结构化文字及必要的 SVG 围栏保留；建议在启用 SVG Editor 插件的 Obsidian 中阅读。每条信息或图表标题末尾的上标数字为页码。
>
> 提取进度：……（已提取至第 N 页）

---

## 第一部　部名（第37—152页）

### 1　章节名称（第37—52页）

_（待提取）_

### 2　章节名称（第53—62页）

> 已提取内容…… ⁵⁵
```

Rules:

- Keep the complete TOC outline and locked ranges.
- Embed text and visual units under their chapters in page order.
- Leave `_（待提取）_` under chapters not yet covered.
- Update the progress marker.
- Default to one self-contained `.md` file with no asset folder.
- In optional evidence mode only, use a sibling `figures/` directory with stable relative links.

## 5. Recognition notes

Append only when needed:

```markdown
识别说明：
- 页码/章节归属不确定：……
- OCR 疑似：……
- 图表边界/关系不确定：……
- 图表画面问题（截断、阴影、虚焦、透视、遮挡）：……
- 待拼接文字/跨页图表：……
- 缺失图例/单位/来源/图注：……
- 采用文字降级而未生成 SVG：……
```

Keep notes factual. Do not explain or interpret the author's claims.
