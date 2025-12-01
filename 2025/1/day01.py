## Pull Data
from pathlib import Path

from get_data import save_data, timeit

save_data(year := 2025, day := 1)
data = Path(f"{year}/{day}/day{day:02d}.txt").read_text()
# data = Path(f"{year}/{day}/day{day:02d}_sample.txt").read_text()
track_length = 100


## Part 1
@timeit
def part1(data=data, position=50):
    laps_completed = 0

    for line in data.splitlines():
        if not line:
            continue

        delta = int(line[1:]) * (1 if line[0] == "R" else -1)
        position = (position + delta) % track_length
        laps_completed += position == 0

    return laps_completed


print(part1())


## Part 2
def part2(data=data, position=50):
    zero_passed = 0

    for line in data.splitlines():
        distance = int(line[1:])

        zero_passed += distance // track_length

        distance %= track_length
        distance = distance * (1 if line[0] == "R" else -1)

        old_position = position
        position += distance

        if position > track_length:
            zero_passed += 1
        # No double-counting
        if old_position != 0 and position < 0:
            zero_passed += 1

        position %= track_length

        if position == 0:
            zero_passed += 1

    return zero_passed


print(part2())
