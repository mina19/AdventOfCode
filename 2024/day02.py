from pathlib import Path

import numpy as np

## Pull Data
from get_data import save_data, timeit

save_data(2024, day := 2)

## Part 1
data = Path(f"day{day:02d}.txt").read_text().splitlines()
data = [[int(num) for num in nums_list.split()] for nums_list in data]


def count_violations(num_list):
    # The levels are either all increasing or all decreasing.
    # Any two adjacent levels differ by at least one and at most three.
    diff_list = np.diff(num_list)
    mostly_positive = len([x for x in diff_list if x > 0]) > len(
        [x for x in diff_list if x < 0]
    )
    if mostly_positive:
        return len([x for x in diff_list if x <= 0 or x > 3])
    else:
        return len([x for x in diff_list if x >= 0 or x < -3])


@timeit
def part1():
    violations_count_list = [count_violations(line) for line in data]
    print(violations_count_list.count(0))
    return violations_count_list


# Part 2
def recount_violations(num_list):
    for i in range(len(num_list)):
        variant = np.concatenate((num_list[:i], num_list[i + 1 :]))
        violation_count = count_violations(variant)
        if violation_count == 0:
            return 0
    return violation_count


@timeit
def part2():
    violations_count_list = part1()

    filtered_data = [
        num_list for num_list, marker in zip(data, violations_count_list) if marker > 0
    ]

    violations_recount_list = [
        recount_violations(num_list) for num_list in filtered_data
    ]
    print(violations_count_list.count(0) + violations_recount_list.count(0))


part2()
