## Pull Data
from pathlib import Path

from get_data import save_data, timeit
from collections import defaultdict
from itertools import combinations

save_data(2024, day := 8)
data = Path(f"2024/8/day{day:02d}.txt").read_text().splitlines()
# data = Path(f"2024/8/day{day:02d}_sample.txt").read_text().splitlines()

# Shape of data
rows = len(data)
cols = len(data[0])

# Hash the data. If we hit a boundary return !
data_dict = defaultdict(
    lambda: defaultdict(lambda: "!"),  # Invalid row
    enumerate(
        defaultdict((lambda: "!"), enumerate(line)) for line in data
    ),  # Invalid column
)


# Helper functions
def find_frequencies():
    # Single lowercase letter, uppercase letter, or digit
    # First find all valid positions
    positions = [
        (row, col, value)
        for row, row_dict in data_dict.items()
        for col, value in row_dict.items()
        if value.islower() or value.isupper() or value.isdigit()
    ]

    # Create frequency dictionary
    frequency_dict = defaultdict(lambda: [])
    for row, col, value in positions:
        frequency_dict[value].append((row, col))

    return frequency_dict


frequency_dict = find_frequencies()


def find_antinodes(pair):
    row1, col1 = pair[0]
    row2, col2 = pair[1]

    drow = row2 - row1
    dcol = col2 - col1

    # Point before pair[0]
    point_before = (row1 - drow, col1 - dcol)

    # Point after pair[1]
    point_after = (row2 + drow, col2 + dcol)

    return [point_before, point_after]


def find_antinodes_resonant_harmonics(pair):
    row1, col1 = pair[0]
    row2, col2 = pair[1]

    drow = row2 - row1
    dcol = col2 - col1

    points = []
    # Points before pair[0]
    curr_row, curr_col = row1 - drow, col1 - dcol
    while 0 <= curr_row < rows and 0 <= curr_col < cols:
        points.append((curr_row, curr_col))
        curr_row -= drow
        curr_col -= dcol

    # Point after pair[1]
    curr_row, curr_col = row2 + drow, col2 + dcol
    while 0 <= curr_row < rows and 0 <= curr_col < cols:
        points.append((curr_row, curr_col))
        curr_row += drow
        curr_col += dcol

    return points


## Part 1
def find_all_antinodes(resonant_harmonics=True):
    # Now includes resonant harmonics lol
    frequency_dict = find_frequencies()

    # First find all pairs for each frequency
    all_pairs = {
        frequency_key: list(combinations(coords, 2))
        for frequency_key, coords in frequency_dict.items()
    }

    # For each pair in frequency find possible antinode positions
    all_antinodes = set()
    # Now add the resonant harmonics
    for pairs in all_pairs.values():
        for pair in pairs:
            points = (
                find_antinodes_resonant_harmonics(pair)
                if resonant_harmonics
                else find_antinodes(pair)
            )
            all_antinodes.update(
                point
                for point in points
                if data_dict[point] != "!"
                and 0 <= point[0] < rows
                and 0 <= point[1] < cols
            )

    # Next include the original antennae locations if resonant harmonics are being found
    if resonant_harmonics:
        for coords in frequency_dict.values():
            all_antinodes.update(coords)

    return all_antinodes


@timeit
def run(resonant_harmonics=True):
    all_antinodes = find_all_antinodes(resonant_harmonics)

    return len(all_antinodes)


# Part 1
print(run(resonant_harmonics=False))

# Part 2
print(run(resonant_harmonics=True))
