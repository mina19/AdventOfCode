## Pull Data
import re
from pathlib import Path

from get_data import save_data, timeit

save_data(2024, day := 3)

data = Path(f"2024/3/day{day:02d}.txt").read_text()

## Part 1
pattern = r"mul\((\d+),(\d+)\)"


@timeit
def part1():
    matches = re.findall(pattern, data)

    total = 0
    for num1, num2 in matches:
        total += int(num1) * int(num2)
    return total


print(part1())

# Part 2


## This is slower than I'd like.
@timeit
def part2_slow():
    do_matches = [(match.start(), "do") for match in re.finditer(r"do\(\)", data)]
    dont_matches = [
        (match.start(), "dont") for match in re.finditer(r"don't\(\)", data)
    ]

    combined_matches = do_matches + dont_matches
    sorted_combined_matches = sorted(combined_matches, key=lambda x: x[0], reverse=True)

    def find_last_instruction(target):
        for t in sorted_combined_matches:
            if t[0] < target:
                return t[1]
        return "do"

    matches = re.finditer(pattern, data)

    total = 0
    for match in matches:
        instruction = find_last_instruction(match.start())
        if instruction == "do":
            total += int(match.group(1)) * int(match.group(2))
    return total


print(part2_slow())


## Another fast way (from Michael C.)
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


## Another fast way (from Matt C.)
@timeit
def part2_fast2():
    matches = re.finditer(r"mul\((\d+),(\d+)\)|don't\(\)|do\(\)", data)

    do_mul = True
    total = 0
    for match in matches:
        if match.group(0) == "don't()":
            do_mul = False
        elif match.group(0) == "do()":
            do_mul = True
        else:
            total += int(match.group(1)) * int(match.group(2)) if do_mul else 0

    return total


print(part2_fast2())
