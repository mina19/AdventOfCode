## Pull Data
import re

from get_data import save_data

day = 3
save_data(2024, day)

## Part 1
lines = [line.rstrip() for line in open(f"day{day:02d}.txt")]

mystr = ""
for line in lines:
    mystr += line

pattern = r"mul\((\d+),(\d+)\)"

matches = re.findall(pattern, mystr)

prod = 0
for num1, num2 in matches:
    prod += int(num1) * int(num2)

print(prod)
