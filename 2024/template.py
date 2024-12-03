## Pull Data
from pathlib import Path

from get_data import save_data, timeit

day = 1
save_data(2024, day)

## Part 1
data = Path(f"day{day:02d}.txt").read_text()
