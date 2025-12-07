## Pull Data
from collections import defaultdict
from pathlib import Path

# from get_data import save_data, timeit

# save_data(year := 2025, day := 7)
year = 2025
day = 7
lines = Path(f"{year}/{day}/day{day:02d}.txt").read_text().splitlines()
# lines = Path(f"{year}/{day}/day{day:02d}_sample.txt").read_text().splitlines()

# Shape of data
rows = len(lines)
cols = len(lines[0])

# Hash the data. If we hit a boundary return !
data_dict = defaultdict(
    lambda: defaultdict(lambda: "!"),  # Invalid row
    enumerate(
        defaultdict((lambda: "!"), enumerate(line)) for line in lines
    ),  # Invalid column
)


## Part 1
# @timeit
def part1():
    start_col = next(col for col in range(cols) if data_dict[0][col] == "S")

    beam_cols = {start_col}
    splits = 0

    for row in range(rows):
        new_beam_cols = set()
        for beam_col in beam_cols:
            if data_dict[row][beam_col] == "^":
                splits += 1
                new_beam_cols.add(beam_col - 1)
                new_beam_cols.add(beam_col + 1)
            else:
                new_beam_cols.add(beam_col)

        beam_cols = new_beam_cols

    return splits


print(part1())


## Part 2
# @timeit
def part2_does_not_scale():
    start_col = next(col for col in range(cols) if data_dict[0][col] == "S")

    # Each beam is now (column, path_tuple)
    beams = {(start_col, ())}

    for row in range(rows):
        beams2 = set()
        for beam_col, path in beams:
            new_path = path + (beam_col,)

            if data_dict[row][beam_col] == "^":
                beams2.add((beam_col + 1, new_path))
                beams2.add((beam_col - 1, new_path))
            else:
                beams2.add((beam_col, new_path))

        beams = beams2

    # Collect all final timelines
    all_timelines = set()
    for beam_col, path in beams:
        final_path = path + (beam_col,)
        all_timelines.add(final_path)

    return len(all_timelines)


def part2_count():
    start_col = next(col for col in range(cols) if data_dict[0][col] == "S")

    memo = {}

    def count_timelines(row, col):
        # Count distinct timelines from this position to the end.
        if (row, col) in memo:
            return memo[row, col]

        # Base case: reached the last row
        if row + 1 == rows:
            return 1

        # Beam continues straight
        if data_dict[row][col] != "^":
            memo[row, col] = count_timelines(row + 1, col)
            return memo[row, col]

        # Split into two timelines
        left_timelines = count_timelines(row + 1, col - 1)
        right_timelines = count_timelines(row + 1, col + 1)
        memo[row, col] = left_timelines + right_timelines
        return memo[row, col]

    return count_timelines(0, start_col)


print(part2_count())
