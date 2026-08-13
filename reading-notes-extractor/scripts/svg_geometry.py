#!/usr/bin/env python3
"""Deterministic geometry helpers for reconstructed SVG diagrams.

The functions are importable, and the small CLI makes the calculations usable
while drafting SVG by hand.  Coordinates are plain SVG user units.
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass
from typing import Sequence


EPSILON = 1e-9


@dataclass(frozen=True)
class Point:
    x: float
    y: float

    def as_list(self) -> list[float]:
        return [round(self.x, 6), round(self.y, 6)]


def _unit(dx: float, dy: float) -> tuple[float, float]:
    length = math.hypot(dx, dy)
    if length <= EPSILON:
        raise ValueError("source and target center must not coincide")
    return dx / length, dy / length


def circle_endpoint(source: Point, center: Point, radius: float, gap: float = 0.0) -> Point:
    """Return a connector endpoint outside a circle, facing ``source``.

    ``gap`` is measured outward from the boundary toward ``source``.  A
    positive gap therefore leaves visible space between line and circle.
    """
    if radius <= 0 or gap < 0:
        raise ValueError("radius must be positive and gap must be non-negative")
    ux, uy = _unit(source.x - center.x, source.y - center.y)
    distance = radius + gap
    return Point(center.x + ux * distance, center.y + uy * distance)


def ellipse_endpoint(
    source: Point,
    center: Point,
    radius_x: float,
    radius_y: float,
    gap: float = 0.0,
) -> Point:
    """Return a connector endpoint outside an axis-aligned ellipse."""
    if radius_x <= 0 or radius_y <= 0 or gap < 0:
        raise ValueError("ellipse radii must be positive and gap non-negative")
    dx, dy = source.x - center.x, source.y - center.y
    if math.hypot(dx, dy) <= EPSILON:
        raise ValueError("source and target center must not coincide")
    scale = 1.0 / math.sqrt((dx * dx) / (radius_x * radius_x) + (dy * dy) / (radius_y * radius_y))
    ux, uy = _unit(dx, dy)
    return Point(center.x + dx * scale + ux * gap, center.y + dy * scale + uy * gap)


def rect_endpoint(
    source: Point,
    center: Point,
    width: float,
    height: float,
    gap: float = 0.0,
) -> Point:
    """Return a connector endpoint outside an axis-aligned rectangle."""
    if width <= 0 or height <= 0 or gap < 0:
        raise ValueError("rectangle dimensions must be positive and gap non-negative")
    dx, dy = source.x - center.x, source.y - center.y
    ux, uy = _unit(dx, dy)
    candidates = []
    if abs(dx) > EPSILON:
        candidates.append((width / 2.0) / abs(dx))
    if abs(dy) > EPSILON:
        candidates.append((height / 2.0) / abs(dy))
    scale = min(candidates)
    return Point(center.x + dx * scale + ux * gap, center.y + dy * scale + uy * gap)


def project(point: Point, offset: Point) -> Point:
    """Project a point by a fixed oblique offset."""
    return Point(point.x + offset.x, point.y + offset.y)


def polygon_orientation(points: Sequence[Point]) -> float:
    """Return twice the signed area; positive means counter-clockwise."""
    if len(points) < 3:
        raise ValueError("a polygon needs at least three points")
    return sum(
        a.x * b.y - b.x * a.y
        for a, b in zip(points, points[1:] + points[:1])
    )


def point_in_convex_polygon(point: Point, polygon: Sequence[Point], tolerance: float = 1e-6) -> bool:
    """Return whether a point lies inside or on a convex polygon."""
    orientation = polygon_orientation(polygon)
    sign = 1.0 if orientation > 0 else -1.0
    for a, b in zip(polygon, polygon[1:] + polygon[:1]):
        cross = (b.x - a.x) * (point.y - a.y) - (b.y - a.y) * (point.x - a.x)
        if sign * cross < -tolerance:
            return False
    return True


def clip_segment_to_convex_polygon(
    start: Point,
    end: Point,
    polygon: Sequence[Point],
    inset: float = 0.0,
) -> tuple[Point, Point] | None:
    """Clip a segment to a convex polygon using parametric half-planes.

    ``inset`` shortens the visible clipped segment at both ends.  It is useful
    when an internal partition should stop just inside a plane outline.
    """
    if inset < 0:
        raise ValueError("inset must be non-negative")
    orientation = polygon_orientation(polygon)
    sign = 1.0 if orientation > 0 else -1.0
    dx, dy = end.x - start.x, end.y - start.y
    t_enter, t_exit = 0.0, 1.0

    for a, b in zip(polygon, polygon[1:] + polygon[:1]):
        ex, ey = b.x - a.x, b.y - a.y
        value_at_start = sign * (ex * (start.y - a.y) - ey * (start.x - a.x))
        slope = sign * (ex * dy - ey * dx)
        if abs(slope) <= EPSILON:
            if value_at_start < 0:
                return None
            continue
        boundary_t = -value_at_start / slope
        if slope > 0:
            t_enter = max(t_enter, boundary_t)
        else:
            t_exit = min(t_exit, boundary_t)
        if t_enter - t_exit > EPSILON:
            return None

    clipped_start = Point(start.x + dx * t_enter, start.y + dy * t_enter)
    clipped_end = Point(start.x + dx * t_exit, start.y + dy * t_exit)
    if inset:
        length = math.hypot(clipped_end.x - clipped_start.x, clipped_end.y - clipped_start.y)
        if length <= 2 * inset + EPSILON:
            return None
        ux = (clipped_end.x - clipped_start.x) / length
        uy = (clipped_end.y - clipped_start.y) / length
        clipped_start = Point(clipped_start.x + ux * inset, clipped_start.y + uy * inset)
        clipped_end = Point(clipped_end.x - ux * inset, clipped_end.y - uy * inset)
    return clipped_start, clipped_end


def parse_point(raw: str) -> Point:
    parts = raw.split(",")
    if len(parts) != 2:
        raise argparse.ArgumentTypeError("point must be x,y")
    try:
        return Point(float(parts[0]), float(parts[1]))
    except ValueError as exc:
        raise argparse.ArgumentTypeError("point coordinates must be numbers") from exc


def parse_polygon(raw: str) -> list[Point]:
    points = [parse_point(item) for item in raw.split(";") if item]
    if len(points) < 3:
        raise argparse.ArgumentTypeError("polygon must contain at least three x,y points")
    return points


def _emit(payload: dict[str, object]) -> None:
    print(json.dumps(payload, ensure_ascii=False, separators=(",", ":")))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    circle = subparsers.add_parser("circle-endpoint")
    circle.add_argument("--source", required=True, type=parse_point)
    circle.add_argument("--center", required=True, type=parse_point)
    circle.add_argument("--radius", required=True, type=float)
    circle.add_argument("--gap", type=float, default=0.0)

    ellipse = subparsers.add_parser("ellipse-endpoint")
    ellipse.add_argument("--source", required=True, type=parse_point)
    ellipse.add_argument("--center", required=True, type=parse_point)
    ellipse.add_argument("--rx", required=True, type=float)
    ellipse.add_argument("--ry", required=True, type=float)
    ellipse.add_argument("--gap", type=float, default=0.0)

    rectangle = subparsers.add_parser("rect-endpoint")
    rectangle.add_argument("--source", required=True, type=parse_point)
    rectangle.add_argument("--center", required=True, type=parse_point)
    rectangle.add_argument("--width", required=True, type=float)
    rectangle.add_argument("--height", required=True, type=float)
    rectangle.add_argument("--gap", type=float, default=0.0)

    clipped = subparsers.add_parser("clip-segment")
    clipped.add_argument("--start", required=True, type=parse_point)
    clipped.add_argument("--end", required=True, type=parse_point)
    clipped.add_argument("--polygon", required=True, type=parse_polygon)
    clipped.add_argument("--inset", type=float, default=0.0)

    projected = subparsers.add_parser("project")
    projected.add_argument("--point", required=True, type=parse_point)
    projected.add_argument("--offset", required=True, type=parse_point)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.command == "circle-endpoint":
        point = circle_endpoint(args.source, args.center, args.radius, args.gap)
        _emit({"point": point.as_list()})
    elif args.command == "ellipse-endpoint":
        point = ellipse_endpoint(args.source, args.center, args.rx, args.ry, args.gap)
        _emit({"point": point.as_list()})
    elif args.command == "rect-endpoint":
        point = rect_endpoint(args.source, args.center, args.width, args.height, args.gap)
        _emit({"point": point.as_list()})
    elif args.command == "clip-segment":
        result = clip_segment_to_convex_polygon(args.start, args.end, args.polygon, args.inset)
        _emit({"segment": None if result is None else [result[0].as_list(), result[1].as_list()]})
    else:
        point = project(args.point, args.offset)
        _emit({"point": point.as_list()})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
