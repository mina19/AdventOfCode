## Pull Data

from functools import lru_cache
from pathlib import Path

from get_data import save_data, timeit

save_data(year := 2025, day := 9)
data = Path(f"{year}/{day}/day{day:02d}.txt").read_text()
# data = Path(f"{year}/{day}/day{day:02d}_sample.txt").read_text()
coords = [tuple(map(int, line.split(","))) for line in data.splitlines()]


## Part 1
@timeit
def part1():
    all_edges = [
        (
            idx1,
            idx2,
            (abs(coord_idx1[0] - coord_idx2[0]) + 1)
            * (abs(coord_idx1[1] - coord_idx2[1]) + 1),
        )
        for idx1, coord_idx1 in enumerate(coords)
        for idx2, coord_idx2 in enumerate(coords[idx1 + 1 :], start=idx1 + 1)
    ]

    all_edges.sort(key=lambda x: x[2], reverse=True)
    _, _, area = all_edges[0]

    return area


print(part1())


## Part 2
@lru_cache
def point_in_polygon(x, y):
    n = len(coords)
    inside = False
    epsilon = 1e-9

    for i in range(n):
        xi, yi = coords[i]
        xj, yj = coords[(i + 1) % n]

        # Check if point is on the edge
        # Calculate cross product for collinearity
        cross_product = (y - yi) * (xj - xi) - (x - xi) * (yj - yi)

        if abs(cross_product) < epsilon:
            # Point is collinear, check if it's within the segment bounds
            if (
                min(xi, xj) - epsilon <= x <= max(xi, xj) + epsilon
                and min(yi, yj) - epsilon <= y <= max(yi, yj) + epsilon
            ):
                return True

        # Ray casting algorithm for interior points
        if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi) + xi):
            inside = not inside

    return inside


@lru_cache
def all_rectangle_points_inside(x1, y1, x2, y2):
    """
    Returns True if all integer points in the rectangle (inclusive) are inside the polygon.
    """
    xmin, xmax = min(x1, x2), max(x1, x2)
    ymin, ymax = min(y1, y2), max(y1, y2)
    for x in range(xmin, xmax + 1):
        for y in range(ymin, ymax + 1):
            if not point_in_polygon(x, y):
                return False
    return True


@timeit
def part2():
    all_edges = [
        (
            idx1,
            idx2,
            (abs(coord_idx1[0] - coord_idx2[0]) + 1)
            * (abs(coord_idx1[1] - coord_idx2[1]) + 1),
        )
        for idx1, coord_idx1 in enumerate(coords)
        for idx2, coord_idx2 in enumerate(coords[idx1 + 1 :], start=idx1 + 1)
    ]

    all_edges.sort(key=lambda x: x[2], reverse=True)

    best_area = 0
    best_corners = None

    for coord_idx1, coord_idx2, edge_area in all_edges:
        p1 = coords[coord_idx1]
        p2 = coords[coord_idx2]

        # Skip if area is smaller than current best
        if edge_area <= best_area:
            break  # Can break since list is sorted

        # Check if all points in rectangle are inside polygon
        if all_rectangle_points_inside(p1[0], p1[1], p2[0], p2[1]):
            best_area = edge_area
            best_corners = (p1, p2)

    return best_corners, best_area


print(part2())
