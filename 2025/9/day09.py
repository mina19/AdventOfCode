## Pull Data

from functools import lru_cache
from pathlib import Path

# from get_data import save_data, timeit

# save_data(year := 2025, day := 9)
year = 2025
day = 9
data = Path(f"{year}/{day}/day{day:02d}.txt").read_text()
# data = Path(f"{year}/{day}/day{day:02d}_sample.txt").read_text()
coords = [tuple(map(int, line.split(","))) for line in data.splitlines()]


## Part 1
# @timeit
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
    Returns True if all integer points on the rectangle perimeter (inclusive) are inside the polygon.
    """
    xmin, xmax = min(x1, x2), max(x1, x2)
    ymin, ymax = min(y1, y2), max(y1, y2)

    # Check top and bottom edges
    for x in range(xmin, xmax + 1):
        if not point_in_polygon(x, ymin):
            return False
        if not point_in_polygon(x, ymax):
            return False

    # Check left and right edges (excluding corners already checked)
    for y in range(ymin + 1, ymax):
        if not point_in_polygon(xmin, y):
            return False
        if not point_in_polygon(xmax, y):
            return False

    return True


# @timeit
def part2_did_not_scale():
    candidates = [
        (
            idx1,
            idx2,
            (abs(coord_idx1[0] - coord_idx2[0]) + 1)
            * (abs(coord_idx1[1] - coord_idx2[1]) + 1),
        )
        for idx1, coord_idx1 in enumerate(coords)
        for idx2, coord_idx2 in enumerate(coords[idx1 + 1 :], start=idx1 + 1)
    ]

    candidates.sort(key=lambda x: x[2], reverse=True)

    best_area = 0
    best_corners = None

    for coord_idx1, coord_idx2, area in candidates:
        p1 = coords[coord_idx1]
        p2 = coords[coord_idx2]

        # Skip if area is smaller than current best
        if area <= best_area:
            break

        if all_rectangle_points_inside(p1[0], p1[1], p2[0], p2[1]):
            best_area = area
            best_corners = (p1, p2)

            return best_corners, best_area
    
    return None, 0


### New method
def check_rectangle_in_rectilinear_polygon(x1, y1, x2, y2):
    xmin, xmax = min(x1, x2), max(x1, x2)
    ymin, ymax = min(y1, y2), max(y1, y2)

    test_xs = set([xmin, xmax])
    test_ys = set([ymin, ymax])
    
    for x, y in coords:
        if xmin <= x <= xmax:
            test_xs.add(x)
        if ymin <= y <= ymax:
            test_ys.add(y)
    
    test_xs = sorted(test_xs)
    test_ys = sorted(test_ys)
    
    # Check all corners first
    if not all(point_in_polygon(x, y) for x, y in 
               [(xmin, ymin), (xmin, ymax), (xmax, ymin), (xmax, ymax)]):
        return False
    
    # Check perimeter at critical coordinates
    # Top and bottom edges
    for x in test_xs:
        if not point_in_polygon(x, ymin) or not point_in_polygon(x, ymax):
            return False
    
    # Left and right edges
    for y in test_ys:
        if not point_in_polygon(xmin, y) or not point_in_polygon(xmax, y):
            return False
    
    return True

# @timeit
def part2():
    candidates = [
        (
            idx1,
            idx2,
            (abs(coord_idx1[0] - coord_idx2[0]) + 1)
            * (abs(coord_idx1[1] - coord_idx2[1]) + 1),
        )
        for idx1, coord_idx1 in enumerate(coords)
        for idx2, coord_idx2 in enumerate(coords[idx1 + 1 :], start=idx1 + 1)
    ]

    candidates.sort(key=lambda x: x[2], reverse=True)
    
    for idx, (i, j, area) in enumerate(candidates):
        if idx % 1000 == 0 and idx > 0:
            print(f"Checked {round(idx/len(candidates) * 100)}% of candidates...")
        
        x1, y1 = coords[i]
        x2, y2 = coords[j]
        
        if check_rectangle_in_rectilinear_polygon(x1, y1, x2, y2):
            return ((x1, y1), (x2, y2)), area
    
    return None, 0

print(part2())