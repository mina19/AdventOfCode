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

directions = [(0, 1), (0, -1), (-1, 0), (1, 0)]
diagonals = [(-1, -1), (1, 1), (-1, 1), (1, -1)]


def determine_new_region(
    start_row, start_col, region_number, visited_region_map, part2=False
):
    # Since we pop and append on opposite sides this is a BFS
    region_character = data_dict[start_row][start_col]

    visited = set()
    q = deque()
    q.append((start_row, start_col))
    area = 0
    sides_or_perimeter = 0
    while q:
        row, col = q.popleft()
        if (row, col) in visited:
            continue

        visited.add((row, col))
        visited_region_map[row][col] = region_number
        # Increment area since item was added to deque only if it matched the region character
        area += 1
        for drow, dcol in directions:
            if data_dict[row + drow][col + dcol] == region_character:
                q.append((row + drow, col + dcol))
            else:
                # For part 1 we care about the perimeter.
                # Since the character is different, this is a boundary
                # and we need to increment the perimeter
                if not part2:
                    sides_or_perimeter += 1
        if part2:
            # Instead of using the perimeter to calculate the price,
            # you need to use the number of sides each region has.
            for drow, dcol in diagonals:
                # Case 1: Corner is different but both adjacent cells match
                # A A
                # A B
                if (
                    data_dict[row + drow][col + dcol] != region_character
                    and data_dict[row + drow][col] == region_character
                    and data_dict[row][col + dcol] == region_character
                ):
                    sides_or_perimeter += 1
                # Case 2: Both adjacent cells are different
                # A B
                # B A
                elif (
                    data_dict[row + drow][col] != region_character
                    and data_dict[row][col + dcol] != region_character
                ):
                    sides_or_perimeter += 1
    return sides_or_perimeter, area


@timeit
def solve(part2=False):
    result = 0
    region_number = 0

    # Keep track of visted areas
    # -1 if not visited, otherwise replace with assigned region #
    visited_region_map = [[-1 for col in range(cols)] for row in range(rows)]

    for row in range(rows):
        for col in range(cols):
            if visited_region_map[row][col] == -1:  # Unvisited so find new region
                if not part2:
                    perimeter, area = determine_new_region(
                        row, col, region_number, visited_region_map
                    )
                    result += perimeter * area
                else:
                    sides, area = determine_new_region(
                        row, col, region_number, visited_region_map, part2=True
                    )
                    result += sides * area
                region_number += 1

    return result


## Part 1
print(solve())


## Part 2
print(solve(part2=True))
