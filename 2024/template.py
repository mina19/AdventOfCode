## Pull Data
from get_data import save_data, timeit

day = 1
save_data(2024, day)

## Part 1
lines = [line.rstrip() for line in open(f"day{day:02d}.txt")]
