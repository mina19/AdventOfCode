## Pull Data
from pathlib import Path

from get_data import save_data, timeit

save_data(year := 2025, day := 1)
data = Path(f"{year}/{day}/day{day:02d}.txt").read_text()
data = Path(f"{year}/{day}/day{day:02d}_sample.txt").read_text()


## Part 1
@timeit
def part1():
    pass


part1()


## Part 2
@timeit
def part2():
    pass


part2()
