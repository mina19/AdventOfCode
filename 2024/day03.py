## Pull Data
import re

from get_data import save_data, timeit

day = 3
save_data(2024, day)

## Part 1
lines = [line.rstrip() for line in open(f"day{day:02d}.txt")]

mystr = ""
for line in lines:
    mystr += line

# mystr = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
pattern = r"mul\((\d+),(\d+)\)"

matches = re.findall(pattern, mystr)
matches = [(int(match[0]), int(match[1])) for match in matches]


@timeit
def part1():
    prod = 0
    for num1, num2 in matches:
        prod += num1 * num2
    return prod


print(part1())

# Part 2
match_positions = [match.start() for match in re.finditer(pattern, mystr)]
mul_dict = dict(zip(match_positions, matches))

do_pattern = r"do\(\)"
dont_pattern = r"don't\(\)"
do_matches = [(match.start(), "do") for match in re.finditer(do_pattern, mystr)]
dont_matches = [(match.start(), "dont") for match in re.finditer(dont_pattern, mystr)]

combined_matches = do_matches + dont_matches
sorted_combined_matches = sorted(combined_matches, key=lambda x: x[0])


def find_last_instruction(target):
    for t in reversed(sorted_combined_matches):
        if t[0] < target:
            return t
    return (0, "do")


@timeit
def part2():
    prod = 0
    for i in range(len(mystr)):
        if i in match_positions:
            match = mul_dict[i]
            instruction = find_last_instruction(i)[1]
            if instruction == "do":
                prod += int(match[0]) * int(match[1])
    return prod


print(part2())
