## Pull Data
import re
from pathlib import Path

from get_data import save_data, timeit

day = 3
save_data(2024, day)

## Part 1
# lines = [line.rstrip() for line in open(f"day{day:02d}.txt")]

# data = ""
# for line in lines:
#     data += line

data = Path(f"day{day:02d}.txt").read_text()

# data = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
pattern = r"mul\((\d+),(\d+)\)"


@timeit
def part1():
    matches = re.findall(pattern, data)
    matches = [(int(match[0]), int(match[1])) for match in matches]

    total = 0
    for num1, num2 in matches:
        total += num1 * num2
    return total


print(part1())

# Part 2
do_pattern = r"do\(\)"
dont_pattern = r"don't\(\)"
do_matches = [(match.start(), "do") for match in re.finditer(do_pattern, data)]
dont_matches = [(match.start(), "dont") for match in re.finditer(dont_pattern, data)]

combined_matches = do_matches + dont_matches
sorted_combined_matches = sorted(combined_matches, key=lambda x: x[0], reverse=True)


def find_last_instruction(target):
    for t in sorted_combined_matches:
        if t[0] < target:
            return t
    return (0, "do")


## This is slower than I'd like.
@timeit
def part2_slow():
    matches = re.finditer(pattern, data)

    total = 0
    for match in matches:
        instruction = find_last_instruction(match.start())
        if instruction[1] == "do":
            total += int(match.group(1)) * int(match.group(2))
    return total


print(part2_slow())


## Faster version
@timeit
def part2_fast():
    matches = re.finditer(pattern, data)

    do = True
    total = 0
    border = 0

    for match in matches:
        dont_ind = data[border : match.start()].find("don't()")
        do_ind = data[border : match.start()].find("do()")

        if dont_ind != -1 and dont_ind > do_ind:
            do = False
        elif do_ind != -1 and do_ind > dont_ind:
            do = True

        if do:
            total += int(match.group(1)) * int(match.group(2))

        border = match.end()

    return total


print(part2_fast())
