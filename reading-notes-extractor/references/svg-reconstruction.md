# Fenced SVG reconstruction for Obsidian

Read this file before reconstructing any chart or diagram as SVG. The aim is an Obsidian-ready information replica, not an artistic redraw. The default consumer is Obsidian with the SVG Editor plugin enabled.

## Fidelity order and stop rule

Preserve, in this order:

1. printed wording, numbers, units, source, and caption;
2. explicit information relationships;
3. topology, grouping, relative position, and direction;
4. visual style.

Do not imitate paper texture, photographed perspective, shadow, blur, or print defects. Never add an unseen arrow, node, cell, value, boundary, or causal relation. If a photograph does not support a reliable topology, stop drawing and use a structured transcription with an uncertainty note.

## Obsidian SVG Editor shell

Put each SVG in its own unindented fenced code block whose language identifier is exactly lowercase `svg`. Do not wrap the fence or SVG in a `div`, `figure`, blockquote, list item, or another HTML element. Keep the opening tag on one line:

````markdown
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 500" width="100%" role="img" aria-labelledby="visual-title visual-desc">
  <title id="visual-title">Printed title or neutral object name</title>
  <desc id="visual-desc">A concise description of the encoded structure.</desc>
  <rect data-role="canvas-background" x="0" y="0" width="800" height="500" fill="#F5F7FA" fill-opacity="1" stroke="#000000" stroke-opacity="0.08" stroke-width="1"/>
  ...
</svg>
```
````

Requirements:

- Include `viewBox`, `width="100%"`, `<title>`, and `<desc>`. Let the plugin derive responsive height from the `viewBox`; do not add a fixed pixel height.
- Make the first graphical child after direct `<title>`/`<desc>` metadata a full-canvas `<rect data-role="canvas-background">` whose `x`/`y` are `0`, whose `width`/`height` equal the `viewBox` dimensions, whose fill is exactly `#F5F7FA` at 100%, and whose stroke is exactly `#000000` at 8% opacity. Use `stroke-width="1"` unless the source requires a different visible frame.
- Use basic SVG elements only: `g`, `line`, `polyline`, `polygon`, `path`, `rect`, `circle`, `ellipse`, and `text`.
- Do not use scripts, external style sheets, external fonts, `foreignObject`, or embedded/external images.
- Because the canvas is intentionally fixed and opaque, do not inherit host-theme color and do not use `currentColor`, CSS variables, `light-dark()`, or host-editor theme classes. Use explicit dark foreground colors inside the SVG: default text/primary strokes `#1F2328`, secondary strokes `#57606A`, muted guides `#8C959F`, and neutral fills such as `#D0D7DE`/`#AFB8C1`. Use opacity only for hierarchy, never to make essential text faint.
- If a source truly uses color as data, pair color with labels, line styles, or patterns. Add `data-allow-fixed-color="true"` to the root only when fixed source colors are necessary and verified.

## Drawing order

Use this order unless the original explicitly requires overlap:

1. background guides and relation lines;
2. shapes, planes, or nodes;
3. internal partitions;
4. labels and values;
5. outer outlines.

The order does not excuse bad geometry. A transparent node still needs a shortened connector.

## Connector endpoints

Connectors must terminate on the boundary of a circle, ellipse, or rectangle, leaving a 2–6 unit visual gap. Do not draw center-to-center lines and hide them with opaque fills.

Use `scripts/svg_geometry.py` for deterministic endpoints:

```bash
python3 scripts/svg_geometry.py circle-endpoint --source 250,220 --center 250,90 --radius 65 --gap 4
python3 scripts/svg_geometry.py ellipse-endpoint --source 250,220 --center 400,150 --rx 75 --ry 50 --gap 4
python3 scripts/svg_geometry.py rect-endpoint --source 250,220 --center 400,150 --width 140 --height 70 --gap 4
```

Tag geometry that the validator should check:

```html
<line data-role="connector" data-from="hub" data-to="node-a" x1="..." y1="..." x2="..." y2="..."/>
<circle data-node-id="node-a" cx="..." cy="..." r="..."/>
```

Omit `data-from` or `data-to` when that endpoint is a free hub rather than a shape. A connector may enter a node only when the printed source clearly shows that semantic.

## Layered and pseudo-3D diagrams

Treat each visible plane as a polygon with one coordinate system. Derive every shared edge and partition from those same coordinates.

- Establish the top, front, and side polygons before adding text.
- Reuse exact endpoints for shared edges; do not redraw almost-equal copies.
- Keep one consistent projection offset for parallel depth edges.
- A partition on a plane must start and end on that plane. Clip it rather than extending it and masking the excess.
- Do not invent vertical elbows, kinks, or depth lines to make a division look three-dimensional.
- Separate semantic flow arrows from decorative depth edges through grouping, opacity, and metadata.

Use the clipping helper when needed:

```bash
python3 scripts/svg_geometry.py clip-segment \
  --start 620,430 --end 555,480 \
  --polygon '390,480;455,430;790,430;725,480' --inset 1
```

Tag plane geometry:

```html
<polygon data-plane-id="range-top" points="390,480 455,430 790,430 725,480"/>
<line data-role="partition" data-plane="range-top" x1="620" y1="430" x2="555" y2="480"/>
```

## Charts and coordinate diagrams

- Encode only printed values. For an unlabeled curve, preserve relative movement without inventing coordinates or interpolation.
- Keep axes, units, legends, baselines, dashed thresholds, and estimate markers if printed.
- Place value labels so they do not collide with marks or each other. When space is tight, enlarge the `viewBox` or move the label outside with a clear leader.
- Use redundant encoding: label every series and distinguish it by shape, dash, or placement as well as tone.
- Follow every statistical SVG with a compact data table when exact printed values exist.

## Text and layout

- Prefer the source label verbatim. Break a label into multiple `<tspan>` rows only where space requires it.
- Give text enough padding from borders and connectors. Do not let a line run through a label.
- Treat proximity and enclosure as relationships. Preserve them before decorative alignment.
- Use relative spatial claims in the structured transcription; do not claim exact scale unless the source supplies it.

## Required validation

After drafting, run:

```bash
python3 scripts/validate_visual_markdown.py path/to/note.md --strict
```

Then inspect the rendered document at normal and enlarged zoom in both Obsidian Live Preview and Reading View, using light and dark application themes. Confirm that SVG Editor renders the fenced block in both modes. Optionally inspect VS Code or Cursor, but those editors may show a code fence unless an SVG-fence extension is installed; the structured transcription remains the portable fallback. The script verifies fence/canvas structure and tagged geometry; visual overlap, semantic fidelity, and comparison with the photograph still require inspection.

The final visual unit must also include a structured transcription so the information survives in editors that do not render fenced SVG.
