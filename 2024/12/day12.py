## Pull Data
from pathlib import Path
from collections import defaultdict, deque

from get_data import save_data, timeit

save_data(2024, day := 12)
data = Path(f"2024/{day}/day{day:02d}.txt").read_text().splitlines()
# data = Path(f"2024/{day}/day{day:02d}_sample.txt").read_text().splitlines()

data_dict = defaultdict(
    (lambda: defaultdict(lambda: "!")),
    enumerate(defaultdict((lambda: "!"), enumerate(line)) for line in data),
)

rows = len(data)
cols = len(data[0])

# Keep track of visted areas
# -1 if not visited, otherwise replace with assigned region #
region = [[-1 for col in range(cols)] for row in range(rows)]
directions = [(0, 1), (0, -1), (-1, 0), (1, 0)]


def determine_new_region(start_row, start_col, region_number):
    # Since we pop and append on opposite sides this is a BFS
    region_character = data_dict[start_row][start_col]

    visited = set()
    q = deque()
    q.append((start_row, start_col))
    perimeter, area = 0, 0
    while q:
        row, col = q.popleft()
        if (row, col) in visited:
            continue

        visited.add((row, col))
        region[row][col] = region_number
        # Increment area since item was added to deque only if it matched the region character
        area += 1
        for drow, dcol in directions:
            if data_dict[row + drow][col + dcol] == region_character:
                q.append((row + drow, col + dcol))
            else:
                # Since the character is different, this is a boundary
                # and we need to increment perimeter
                perimeter += 1
    return perimeter, area


## Part 1
@timeit
def part1():
    result = 0
    region_number = 0

    for row in range(rows):
        for col in range(cols):
            if region[row][col] == -1:  # Unvisited so find new region
                perimeter, area = determine_new_region(row, col, region_number)
                result += perimeter * area
                region_number += 1

    return result


print(part1())


## Part 2
@timeit
def part2():
    pass


part2()
