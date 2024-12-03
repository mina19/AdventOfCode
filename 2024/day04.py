## Pull Data
from pathlib import Path

from get_data import save_data, timeit

save_data(2024, day := 4)
data = Path(f"day{day:02d}.txt").read_text()

## Part 1
