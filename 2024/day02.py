import numpy as np

## Pull Data
from get_data import save_data

day = 2
save_data(2024, day)

## Part 1
lines = [
    line.rstrip()
    for line in open(f"/home/coder/workspace/AdventOfCode/2024/day{day:02d}.txt")
]

lines = [[int(num) for num in line.split()] for line in lines]

# The levels are either all increasing or all decreasing.
# Any two adjacent levels differ by at least one and at most three.


def count_violations(line):
    diff_list = np.diff(line)
    mostly_positive = len([x for x in diff_list if x > 0]) > len(
        [x for x in diff_list if x < 0]
    )
    if mostly_positive:
        return len([x for x in diff_list if x <= 0 or x > 3])
    else:
        return len([x for x in diff_list if x >= 0 or x < -3])


violations_count_list = [count_violations(line) for line in lines]
print(violations_count_list.count(0))

# Part 2
filtered_lines = [
    line for line, marker in zip(lines, violations_count_list) if marker > 0
]


def recount_violations(num_list):
    variants = [
        np.concatenate((num_list[:i], num_list[i + 1 :])) for i in range(len(num_list))
    ]
    for variant in variants:
        violation_count = count_violations(variant)
        if violation_count == 0:
            return 0
    return violation_count


violations_recount_list = [recount_violations(line) for line in filtered_lines]
print(violations_count_list.count(0) + violations_recount_list.count(0))
