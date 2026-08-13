#!/usr/bin/env python3
"""Validate visual-heavy Markdown produced by reading-notes-extractor v1.2.0.

The validator checks portable Markdown tables, Obsidian SVG Editor fences,
fixed SVG canvases, explicit foreground colors, connector endpoints, and
plane-clipped partition lines. Geometric checks use explicit SVG metadata
described in references/svg-reconstruction.md.
"""

from __future__ import annotations

import argparse
import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path

from svg_geometry import Point, point_in_convex_polygon


SVG_BLOCK_RE = re.compile(r"<svg\b[^>]*>.*?</svg>", re.DOTALL | re.IGNORECASE)
CODE_FENCE_RE = re.compile(
    r"^(?P<indent>[ \t]*)```(?P<language>[^\n`]*)\n(?P<body>.*?)\n(?P=indent)```[ \t]*$",
    re.DOTALL | re.MULTILINE,
)
HTML_TABLE_RE = re.compile(r"<table\b[^>]*>.*?</table>", re.DOTALL | re.IGNORECASE)
IMAGE_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
DATA_IMAGE_RE = re.compile(r"data:image/|;base64,", re.IGNORECASE)
TABLE_SEPARATOR_RE = re.compile(
    r"^\s*\|?\s*:?-{3,}:?\s*(?:\|\s*:?-{3,}:?\s*)+\|?\s*$"
)
CANVAS_FILL = "#F5F7FA"
CANVAS_STROKE = "#000000"
CANVAS_STROKE_OPACITY = 0.08


@dataclass
class Finding:
    severity: str
    location: str
    message: str


@dataclass
class Report:
    findings: list[Finding] = field(default_factory=list)
    svg_count: int = 0
    table_count: int = 0
    html_table_count: int = 0

    def error(self, location: str, message: str) -> None:
        self.findings.append(Finding("ERROR", location, message))

    def warn(self, location: str, message: str) -> None:
        self.findings.append(Finding("WARN", location, message))


def local_name(tag: str) -> str:
    return tag.split("}", 1)[-1]


def numeric(element: ET.Element, name: str) -> float:
    value = element.get(name)
    if value is None:
        raise ValueError(f"missing {name}")
    return float(value)


def parse_points(raw: str) -> list[Point]:
    values = [part for part in re.split(r"[\s,]+", raw.strip()) if part]
    if len(values) % 2:
        raise ValueError("points must contain x,y pairs")
    return [Point(float(values[i]), float(values[i + 1])) for i in range(0, len(values), 2)]


def parse_viewbox(raw: str) -> tuple[float, float, float, float]:
    values = [part for part in re.split(r"[\s,]+", raw.strip()) if part]
    if len(values) != 4:
        raise ValueError("viewBox must contain min-x, min-y, width, height")
    parsed = tuple(float(value) for value in values)
    if parsed[2] <= 0 or parsed[3] <= 0:
        raise ValueError("viewBox width and height must be positive")
    return parsed  # type: ignore[return-value]


def approximately(left: float, right: float, tolerance: float = 0.01) -> bool:
    return abs(left - right) <= tolerance


def point_relation_to_shape(point: Point, shape: ET.Element) -> tuple[bool, float]:
    """Return ``(inside, outside_gap)`` for supported node shapes."""
    tag = local_name(shape.tag)
    if tag == "circle":
        cx, cy, radius = numeric(shape, "cx"), numeric(shape, "cy"), numeric(shape, "r")
        delta = ((point.x - cx) ** 2 + (point.y - cy) ** 2) ** 0.5 - radius
        return delta < -0.5, max(0.0, delta)
    if tag == "ellipse":
        cx, cy = numeric(shape, "cx"), numeric(shape, "cy")
        rx, ry = numeric(shape, "rx"), numeric(shape, "ry")
        normalized = (((point.x - cx) / rx) ** 2 + ((point.y - cy) / ry) ** 2) ** 0.5
        delta = (normalized - 1.0) * min(rx, ry)
        return delta < -0.5, max(0.0, delta)
    if tag == "rect":
        x, y = numeric(shape, "x"), numeric(shape, "y")
        width, height = numeric(shape, "width"), numeric(shape, "height")
        dx = max(x - point.x, 0.0, point.x - (x + width))
        dy = max(y - point.y, 0.0, point.y - (y + height))
        inside = x + 0.5 < point.x < x + width - 0.5 and y + 0.5 < point.y < y + height - 0.5
        return inside, (dx * dx + dy * dy) ** 0.5
    raise ValueError(f"unsupported node shape <{tag}>")


def split_unescaped_pipes(line: str) -> list[str]:
    stripped = line.strip()
    if stripped.startswith("|"):
        stripped = stripped[1:]
    if stripped.endswith("|") and not stripped.endswith(r"\|"):
        stripped = stripped[:-1]
    cells, current, escaped = [], [], False
    for char in stripped:
        if escaped:
            current.append(char)
            escaped = False
        elif char == "\\":
            current.append(char)
            escaped = True
        elif char == "|":
            cells.append("".join(current).strip())
            current = []
        else:
            current.append(char)
    cells.append("".join(current).strip())
    return cells


def looks_like_table_row(line: str) -> bool:
    return "|" in line and not line.lstrip().startswith("```")


def validate_tables(text: str, report: Report, path: Path) -> None:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if not TABLE_SEPARATOR_RE.match(line):
            continue
        line_no = index + 1
        if index == 0 or not looks_like_table_row(lines[index - 1]):
            report.error(f"{path}:{line_no}", "table separator has no contiguous header row")
            continue
        header_index = index - 1
        if lines[header_index].lstrip().startswith(">") or line.lstrip().startswith(">"):
            report.error(f"{path}:{line_no}", "Markdown table must not be inside a blockquote")
        if header_index > 0 and lines[header_index - 1].strip():
            report.error(f"{path}:{header_index + 1}", "leave one blank line before a Markdown table")

        expected_cells = len(split_unescaped_pipes(lines[header_index]))
        separator_cells = len(split_unescaped_pipes(line))
        if expected_cells != separator_cells:
            report.error(f"{path}:{line_no}", "header and separator column counts differ")

        cursor = index + 1
        data_rows = 0
        while cursor < len(lines) and lines[cursor].strip() and looks_like_table_row(lines[cursor]):
            if lines[cursor].lstrip().startswith(">"):
                report.error(f"{path}:{cursor + 1}", "Markdown table must not be inside a blockquote")
            cells = len(split_unescaped_pipes(lines[cursor]))
            if cells != expected_cells:
                report.error(
                    f"{path}:{cursor + 1}",
                    f"table row has {cells} cells; expected {expected_cells}; escape literal pipes as \\|",
                )
            data_rows += 1
            cursor += 1
        if data_rows == 0:
            report.error(f"{path}:{line_no}", "table has no contiguous data row")
        if cursor < len(lines) and lines[cursor].strip():
            report.error(f"{path}:{cursor + 1}", "leave one blank line after a Markdown table")
        if cursor + 1 < len(lines) and not lines[cursor].strip() and looks_like_table_row(lines[cursor + 1]):
            report.error(f"{path}:{cursor + 2}", "blank line splits a Markdown table")
        report.table_count += 1


def validate_html_tables(text: str, report: Report, path: Path) -> None:
    for number, block in enumerate(HTML_TABLE_RE.findall(text), start=1):
        location = f"{path}:html-table#{number}"
        try:
            root = ET.fromstring(block)
        except ET.ParseError as exc:
            report.error(location, f"invalid HTML-table structure: {exc}")
            continue
        rows = root.findall(".//tr")
        if not rows:
            report.error(location, "HTML table has no rows")
        for cell in root.findall(".//th") + root.findall(".//td"):
            for attribute in ("rowspan", "colspan"):
                raw = cell.get(attribute)
                if raw is not None and (not raw.isdigit() or int(raw) < 1):
                    report.error(location, f"{attribute} must be a positive integer")
        report.html_table_count += 1


def validate_connector(
    element: ET.Element,
    nodes: dict[str, ET.Element],
    report: Report,
    location: str,
) -> None:
    if local_name(element.tag) != "line":
        report.warn(location, "connector geometry is only auto-checked for <line>; inspect this path manually")
        return
    endpoints = {
        "from": Point(numeric(element, "x1"), numeric(element, "y1")),
        "to": Point(numeric(element, "x2"), numeric(element, "y2")),
    }
    for side in ("from", "to"):
        node_id = element.get(f"data-{side}")
        if not node_id:
            continue
        shape = nodes.get(node_id)
        if shape is None:
            report.error(location, f"connector references unknown node {node_id!r}")
            continue
        try:
            inside, gap = point_relation_to_shape(endpoints[side], shape)
        except ValueError as exc:
            report.error(location, str(exc))
            continue
        if inside:
            report.error(location, f"{side} endpoint penetrates node {node_id!r}")
        elif gap > 12:
            report.warn(location, f"{side} endpoint is {gap:.1f} units away from node {node_id!r}; verify intent")


def validate_partition(
    element: ET.Element,
    planes: dict[str, list[Point]],
    report: Report,
    location: str,
) -> None:
    plane_id = element.get("data-plane")
    if not plane_id:
        report.error(location, "partition line needs data-plane metadata")
        return
    polygon = planes.get(plane_id)
    if polygon is None:
        report.error(location, f"partition references unknown plane {plane_id!r}")
        return
    if local_name(element.tag) != "line":
        report.warn(location, "partition geometry is only auto-checked for <line>; inspect this path manually")
        return
    start = Point(numeric(element, "x1"), numeric(element, "y1"))
    end = Point(numeric(element, "x2"), numeric(element, "y2"))
    if not point_in_convex_polygon(start, polygon, tolerance=1.0):
        report.error(location, f"partition start lies outside plane {plane_id!r}")
    if not point_in_convex_polygon(end, polygon, tolerance=1.0):
        report.error(location, f"partition end lies outside plane {plane_id!r}")


def validate_svg(svg_text: str, report: Report, path: Path, number: int) -> None:
    location = f"{path}:svg#{number}"
    opening_tag = svg_text.split(">", 1)[0] + ">"
    if "\n" in opening_tag:
        report.error(location, "opening <svg ...> tag must stay on one line")
    try:
        root = ET.fromstring(svg_text)
    except ET.ParseError as exc:
        report.error(location, f"invalid SVG XML: {exc}")
        return
    if local_name(root.tag) != "svg":
        report.error(location, "inline visual block did not parse as <svg>")
        return
    if not root.get("viewBox"):
        report.error(location, "SVG needs a viewBox")
        viewbox = None
    else:
        try:
            viewbox = parse_viewbox(root.get("viewBox") or "")
        except ValueError as exc:
            report.error(location, str(exc))
            viewbox = None
    if root.get("width") != "100%":
        report.error(location, 'SVG width must be "100%"')
    if root.get("height") and root.get("height") != "auto":
        report.error(location, "omit fixed SVG height; let SVG Editor derive responsive height from viewBox")

    children = list(root)
    if not any(local_name(child.tag) == "title" for child in children):
        report.error(location, "SVG needs a direct <title>")
    if not any(local_name(child.tag) == "desc" for child in children):
        report.error(location, "SVG needs a direct <desc>")

    graphical_children = [child for child in children if local_name(child.tag) not in {"title", "desc", "metadata"}]
    if not graphical_children:
        report.error(location, "SVG has no graphical content")
    else:
        canvas = graphical_children[0]
        if local_name(canvas.tag) != "rect" or canvas.get("data-role") != "canvas-background":
            report.error(location, "first graphical child must be <rect data-role=\"canvas-background\">")
        else:
            if (canvas.get("fill") or "").upper() != CANVAS_FILL:
                report.error(location, f"canvas fill must be {CANVAS_FILL} at 100%")
            try:
                fill_opacity = float(canvas.get("fill-opacity", "1"))
                if not approximately(fill_opacity, 1.0):
                    report.error(location, "canvas fill-opacity must be 1 (100%)")
            except ValueError:
                report.error(location, "canvas fill-opacity must be numeric")
            if (canvas.get("stroke") or "").upper() != CANVAS_STROKE:
                report.error(location, f"canvas stroke must be {CANVAS_STROKE}")
            try:
                stroke_opacity = float(canvas.get("stroke-opacity", ""))
                if not approximately(stroke_opacity, CANVAS_STROKE_OPACITY):
                    report.error(location, "canvas stroke-opacity must be 0.08 (8%)")
            except ValueError:
                report.error(location, "canvas stroke-opacity must be numeric and equal to 0.08")
            if viewbox is not None:
                expected = {"x": viewbox[0], "y": viewbox[1], "width": viewbox[2], "height": viewbox[3]}
                for attribute, expected_value in expected.items():
                    try:
                        actual = numeric(canvas, attribute)
                    except ValueError as exc:
                        report.error(location, f"canvas background {exc}")
                        continue
                    if not approximately(actual, expected_value):
                        report.error(location, f"canvas {attribute} must match viewBox ({expected_value:g})")

    forbidden = {"script", "foreignObject", "image"}
    for element in root.iter():
        tag = local_name(element.tag)
        if tag in forbidden:
            report.error(location, f"portable SVG must not contain <{tag}>")
        for attr_name, attr_value in element.attrib.items():
            if attr_name.endswith("href") and re.match(r"(?:https?:|data:|file:)", attr_value, re.IGNORECASE):
                report.error(location, "SVG must not load external or embedded resources")

    if re.search(r"\bcurrentColor\b", svg_text, re.IGNORECASE):
        report.error(location, "do not inherit currentColor on the fixed light canvas; use explicit dark foreground colors")
    if re.search(r"var\s*\(--", svg_text, re.IGNORECASE):
        report.error(location, "do not use host CSS variables inside fenced SVG")
    if "light-dark(" in svg_text:
        report.error(location, "do not rely on CSS light-dark() inside fenced SVG")

    nodes: dict[str, ET.Element] = {}
    planes: dict[str, list[Point]] = {}
    for element in root.iter():
        node_id = element.get("data-node-id")
        if node_id:
            if node_id in nodes:
                report.error(location, f"duplicate data-node-id {node_id!r}")
            nodes[node_id] = element
        plane_id = element.get("data-plane-id")
        if plane_id:
            if local_name(element.tag) != "polygon":
                report.error(location, "data-plane-id must be attached to a <polygon>")
            else:
                try:
                    planes[plane_id] = parse_points(element.get("points") or "")
                except ValueError as exc:
                    report.error(location, f"invalid plane {plane_id!r}: {exc}")

    for element in root.iter():
        role = element.get("data-role")
        try:
            if role == "connector":
                validate_connector(element, nodes, report, location)
            elif role == "partition":
                validate_partition(element, planes, report, location)
        except ValueError as exc:
            report.error(location, f"invalid geometry metadata: {exc}")


def validate_file(path: Path, allow_images: bool) -> Report:
    report = Report()
    text = path.read_text(encoding="utf-8")
    if DATA_IMAGE_RE.search(text):
        report.error(str(path), "embedded data images/Base64 are not allowed")
    image_links = IMAGE_RE.findall(text)
    if image_links and not allow_images:
        report.error(str(path), "Markdown image links are disabled in the default single-file output")
    validate_tables(text, report, path)
    validate_html_tables(text, report, path)
    fenced_svg_blocks: list[str] = []
    svg_fenced_ranges: list[tuple[int, int]] = []
    for match in CODE_FENCE_RE.finditer(text):
        language = match.group("language").strip()
        if language.lower() != "svg":
            continue
        svg_fenced_ranges.append(match.span())
        if language != "svg":
            report.error(f"{path}:svg-fence", 'SVG fence language must be exactly lowercase "svg"')
        if match.group("indent"):
            report.error(f"{path}:svg-fence", "SVG fence must not be indented")
        body = match.group("body").strip()
        blocks = SVG_BLOCK_RE.findall(body)
        if len(blocks) != 1 or body != blocks[0].strip():
            report.error(f"{path}:svg-fence", "each svg fence must contain exactly one complete <svg> element and no wrapper text")
            continue
        fenced_svg_blocks.append(blocks[0])

    def inside_any_fence(start: int, end: int) -> bool:
        return any(fence_start <= start and end <= fence_end for fence_start, fence_end in svg_fenced_ranges)

    for match in SVG_BLOCK_RE.finditer(text):
        if not inside_any_fence(*match.span()):
            report.error(str(path), "raw inline <svg> is not allowed; wrap it in an unindented lowercase ```svg fence")

    report.svg_count = len(fenced_svg_blocks)
    for number, block in enumerate(fenced_svg_blocks, start=1):
        validate_svg(block, report, path, number)
    return report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="+", type=Path)
    parser.add_argument("--allow-images", action="store_true", help="allow optional evidence image links")
    parser.add_argument("--strict", action="store_true", help="treat warnings as failures")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    failed = False
    for path in args.files:
        if not path.is_file():
            print(f"ERROR {path}: file not found")
            failed = True
            continue
        report = validate_file(path, args.allow_images)
        for finding in report.findings:
            print(f"{finding.severity} {finding.location}: {finding.message}")
        errors = sum(finding.severity == "ERROR" for finding in report.findings)
        warnings = sum(finding.severity == "WARN" for finding in report.findings)
        print(
            f"OK {path}: {report.svg_count} SVG, {report.table_count} Markdown table(s), "
            f"{report.html_table_count} HTML table(s), {errors} error(s), {warnings} warning(s)"
        )
        if errors or (args.strict and warnings):
            failed = True
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
