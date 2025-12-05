## Pull Data
from pathlib import Path

from get_data import save_data, timeit

save_data(year := 2025, day := 5)
data = Path(f"{year}/{day}/day{day:02d}.txt").read_text()
# data = Path(f"{year}/{day}/day{day:02d}_sample.txt").read_text()


## Part 1
@timeit
def part1():
    fresh_id_ranges = data.split("\n\n")[0].splitlines()
    available_ids = data.split("\n\n")[1].splitlines()

    ranges = [
        (int(a), int(b)) for a, b in [line.split("-") for line in fresh_id_ranges]
    ]
    result = 0

    for id in available_ids:
        id = int(id)
        if any(id >= r[0] and id <= r[1] for r in ranges):
            result += 1

    return result


print(part1())


## Part 2
@timeit
def part2():
    fresh_id_ranges = data.split("\n\n")[0].splitlines()
    ranges = [
        (int(a), int(b)) for a, b in [line.split("-") for line in fresh_id_ranges]
    ]
    ranges.sort()

    # Merge overlapping ranges, probably faster way to do this
    while True:
        did_change = False
        num_ranges = len(ranges)
        for i in range(num_ranges - 1):
            a_start, a_end = ranges[i]
            b_start, b_end = ranges[i + 1]
            if a_end >= b_start:
                ranges[i] = (a_start, max(a_end, b_end))
                ranges.pop(i + 1)
                did_change = True
                break
        if not did_change:
            break

    result = 0
    for range_start, range_end in ranges:
        result += range_end - range_start + 1

    return result


print(part2())
