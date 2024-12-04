## Pull Data
from pathlib import Path

from get_data import save_data, timeit

save_data(2024, day := 5)
data = Path(f"day{day:02d}.txt").read_text()

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
