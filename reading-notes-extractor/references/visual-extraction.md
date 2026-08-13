# Visual-object extraction

Read this file whenever a selected page contains a table, matrix, chart, diagram, map, timeline, screenshot, illustration, or other visual object. Read `svg-reconstruction.md` too before producing fenced SVG.

## 1. Selection scope

A star, arrow, check, circle, bracket, side-bar, or handwritten symbol that clearly points to a visual selects the whole object. Strip the reader's mark and include every required attachment; individual labels do not need separate marks.

An explicit request for **all visuals** selects every visual on every supplied photo, including unmarked ones and multiple objects on one page. If the user says that every uploaded photo contains a visual to extract, preserve that rule for the current book session until they change it. This expanded scope applies only to visuals; ordinary prose still follows physical-mark rules.

If a mark may point to either prose or a visual, use direction, proximity, and enclosure. Report unresolved ambiguity rather than deciding silently.

## 2. Visual semantic unit

Keep these parts together:

1. **Core visual:** cells, nodes, connectors, groups, axes, scales, encoded shapes, and readable values.
2. **Required attachments:** figure/table number, title/caption, legend, units, source, footnotes, callouts, and annotations printed as part of the visual.
3. **Structured transcription:** a searchable, neutral account of the rows, columns, nodes, relationships, layers, directions, or printed data.
4. **Direct associated explanation:** the minimum nearby complete sentence(s) that explicitly introduce or decode the visual. Label them `Associated explanation:`.
5. **Recognition notes:** concrete uncertainty, damage, clipping, or missing evidence.

Ordinary nearby exposition does not become selected merely because it discusses the figure. If independently marked prose follows the visual, introduce it with `Other independently marked text:`. Include a sentence that qualifies for both categories once, under associated explanation.

## 3. Default preservation format

The default deliverable is **one Markdown file with no screenshots, image links, or Base64 data**. Preserve the visual through structured text and, when justified, SVG in an Obsidian SVG Editor-compatible `svg` fence. Every SVG uses the fixed light canvas and explicit foreground palette in `svg-reconstruction.md`. This keeps the note searchable, copyable, compact, and readable across Obsidian views and themes.

The source photograph remains evidence for recognition and visual comparison, but it is not copied into the default deliverable. A crop is optional evidence only when the user explicitly asks to retain visual evidence. In that mode, save one faithful final crop per object; use only non-generative rotation, perspective, illumination, or contrast corrections; never use inpainting or invented repairs.

Keep four layers distinct:

- **transcription:** printed wording only;
- **structure:** neutral spatial/relational encoding;
- **associated explanation:** directly related printed prose;
- **recognition notes:** uncertainty and damage.

## 4. Representation routing

Choose the least lossy form:

| Visual type | Default representation |
|---|---|
| Simple table, matrix, comparison grid | Markdown table with contiguous rows. |
| Merged cells or multilevel headers | HTML table only when spans are certain; otherwise nested transcription. Never flatten an ambiguous hierarchy. |
| Statistical chart | Fenced SVG plus an exact-value data table when printed values exist. |
| Quadrant, coordinate, positioning, timeline | Fenced SVG plus structured transcription. |
| Layered model, radial model, architecture, conceptual topology | Fenced SVG plus node/relationship/layer transcription. |
| Flowchart, causal/path diagram | Fenced SVG preferred. Use Mermaid only when automatic layout does not change the source morphology. |
| Tree, hierarchy, taxonomy | Indented outline when morphology is not meaningful; otherwise fenced SVG. |
| Formula or annotated equation | LaTeX plus verbatim variable definitions, only when complete notation is readable. |
| Photograph, advertisement, screenshot, complex illustration | Caption, readable printed text, source, and neutral object transcription. Do not force a redraw. |
| Map or unclear complex visual | Structured transcription. Add SVG only when boundaries and labels are clear. |

Never force a text-heavy visual into a table, or force a photograph into an invented diagram.

## 5. Extraction procedure

For each selected visual:

1. Record why it is selected: physical object-level mark or persistent all-visuals scope.
2. Establish the boundary and all required attachments.
3. Read the page number and file it by the locked TOC range.
4. Transcribe printed labels, values, units, and source **before** reconstructing geometry.
5. Classify the object and apply the routing table.
6. Verify row/column membership, endpoints, arrow direction, grouping, layer order, legend mapping, axis direction, and unit placement.
7. Capture and separately label only the minimum direct associated explanation.
8. Append the superscript page number to the visual heading and separately quoted explanations.
9. Add concrete recognition notes for every uncertain character, boundary, relationship, or attachment.
10. Run the three quality gates below and `scripts/validate_visual_markdown.py` before delivery.

Multiple numbered objects on one page remain separate units. Objects that truly share one caption or legend remain one unit. Hold a cross-page visual until all parts arrive or mark it `[visual truncated; continuation pending]`.

## 6. Fidelity and degradation rules

Preserve in this order: printed text/data/source → explicit relationships → topology and relative position → style.

- Do not infer exact values from bar height, line position, area, angle, color, or map shading.
- Describe an unlabeled curve only by its visible relative movement.
- Do not convert proximity into causality or repair unseen arrows, nodes, cells, lines, labels, or data.
- Do not regularize repeated wording, punctuation, capitalization, or missing cells from neighboring patterns.
- Do not treat shadow, bleed-through, folds, or handwriting as printed encoding.
- Use `[unreadable]`, `[relationship uncertain]`, `[visual partially clipped]`, or a working-language equivalent.
- When topology is uncertain, degrade to structured transcription rather than creating a plausible but wrong SVG.
- The source photograph may validate the reconstruction; it does not authorize copying the crop into the deliverable.

## 7. Three quality gates

### Content gate

- Every selected object is present, including multiple objects on one page.
- Caption, labels, values, units, legend, source, and visual-specific footnotes are complete.
- The visual and structured transcription agree exactly.
- No value, relationship, or attachment was inferred.

### Geometry gate

- Connectors terminate at shape boundaries with a small gap; none penetrates a node unless printed that way.
- Shared edges reuse identical coordinates.
- Plane partitions are derived from and clipped to their plane.
- Projection direction and depth offsets are consistent.
- Text does not collide with lines, marks, or borders.
- Decorative depth lines and semantic arrows remain distinguishable.

### Rendering gate

- Markdown tables render as tables in Obsidian, VS Code, and Cursor.
- SVG is inside a lowercase, unindented `svg` fence and contains no external images or Base64.
- The fixed `#F5F7FA` canvas, 8%-opacity black frame, and explicit dark foreground stay legible in Obsidian Live Preview and Reading View under light and dark application themes.
- The reconstruction has been compared with the source photograph for labels, data, relations, and morphology.

Run:

```bash
python3 scripts/validate_visual_markdown.py path/to/note.md --strict
```

The script covers deterministic portability and tagged geometry. Cross-editor rendering and source comparison remain required visual checks.
