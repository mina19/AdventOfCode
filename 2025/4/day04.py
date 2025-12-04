## Pull Data
from collections import defaultdict
from pathlib import Path

from get_data import save_data, timeit

save_data(year := 2025, day := 4)
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
directions = [(0, 1), (0, -1), (-1, 0), (1, 0), (-1, -1), (1, 1), (-1, 1), (1, -1)]


## Part 1
@timeit
def part1():
    result = 0

    for row in range(rows):
        for col in range(cols):
            if data_dict[row][col] != "@":
                continue
            rolls = 0
            for drow, dcol in directions:
                if data_dict[row + drow][col + dcol] == "@":
                    rolls += 1
            if rolls < 4:
                result += 1

    return result


print(part1())


## Part 2
@timeit
def part2():
    result = 0

    while True:
        rolls_to_remove = []
        for row in range(rows):
            for col in range(cols):
                if data_dict[row][col] != "@":
                    continue
                rolls = 0
                for drow, dcol in directions:
                    if data_dict[row + drow][col + dcol] == "@":
                        rolls += 1
                if rolls < 4:
                    rolls_to_remove.append((row, col))
        if len(rolls_to_remove) == 0:
            break
        result += len(rolls_to_remove)
        for row, col in rolls_to_remove:
            data_dict[row][col] = "."
    return result


print(part2())
