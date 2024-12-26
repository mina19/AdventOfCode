## Pull Data
from collections import defaultdict
from pathlib import Path

from get_data import save_data, timeit

save_data(2024, day := 25)
data = Path(f"2024/{day}/day{day:02d}.txt").read_text().split("\n\n")
# data = Path(f"2024/{day}/day{day:02d}_sample.txt").read_text().split("\n\n")

rows = len(data[0].splitlines())
cols = len(data[0].splitlines()[0])


## Part 1
@timeit
def part1():
    keys = []
    locks = []

    for schematic in data:
        lines = schematic.splitlines()
        grid = defaultdict(
            lambda: defaultdict(lambda: "!"),
            enumerate(defaultdict(lambda: "!", enumerate(line)) for line in lines),
        )
        counts = []
        for col in range(cols):
            count = -1
            for row in range(rows):
                if grid[row][col] == "#":
                    count += 1
            counts.append(count)
        if lines[0] == ".....":
            keys.append(counts)
        else:
            locks.append(counts)

    def check_fit(key, lock):
        for col in range(cols):
            if key[col] + lock[col] >= rows - 1:
                return False
        return True

    result = 0
    for key in keys:
        for lock in locks:
            if check_fit(key, lock):
                result += 1

    return result


print(part1())


## Part 2
@timeit
def part2():
    pass


part2()
