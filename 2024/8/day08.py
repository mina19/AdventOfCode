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


## Part 1
def find_antinodes_pt1():
    # An antinode occurs at any point that is perfectly
    # in line with two antennas of the same frequency
    # - but only when one of the antennas is twice as
    # far away as the other.
    # This means that for any pair of antennas with the
    # same frequency, there are two antinodes, one on either side of them.

    frequency_dict = find_frequencies()

    # First find all pairs for each frequency
    all_pairs = {
        frequency_key: list(combinations(coords, 2))
        for frequency_key, coords in frequency_dict.items()
    }

    # For each pair in frequency find possible antinode positions
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

    all_antinodes = set()
    for pairs in all_pairs.values():
        for pair in pairs:
            points = find_antinodes(pair)
            all_antinodes.update(
                point
                for point in points
                if data_dict[point] != "!"
                and 0 <= point[0] < rows
                and 0 <= point[1] < cols
            )

    return all_antinodes


@timeit
def part1():
    all_antinodes = find_antinodes_pt1()
    return len(all_antinodes)


print(part1())


## Part 2
def find_antinodes_pt2():
    # Now includes resonant harmonics lol
    frequency_dict = find_frequencies()

    # First find all pairs for each frequency
    all_pairs = {
        frequency_key: list(combinations(coords, 2))
        for frequency_key, coords in frequency_dict.items()
    }

    # For each pair in frequency find possible antinode positions
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

    all_antinodes = set()
    for pairs in all_pairs.values():
        for pair in pairs:
            points = find_antinodes_resonant_harmonics(pair)
            all_antinodes.update(
                point
                for point in points
                if data_dict[point] != "!"
                and 0 <= point[0] < rows
                and 0 <= point[1] < cols
            )

    return all_antinodes


@timeit
def part2():
    # Rewrite later. no time rn :-(
    all_antinodes = find_antinodes_pt2()
    original_antennas = set()
    for coords in frequency_dict.values():
        original_antennas.update(coords)

    return len(list(all_antinodes.union(original_antennas)))


print(part2())
