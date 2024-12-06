## Pull Data
from pathlib import Path

from get_data import save_data

save_data(2024, day := 1)

## Part 1
data = Path(f"day{day:02d}.txt").read_text().splitlines()
left = [int(nums.split()[0]) for nums in data]
right = [int(nums.split()[1]) for nums in data]

diffs = [abs(a - b) for a, b in zip(sorted(left), sorted(right))]
print(sum(diffs))


## Part 2
counts_multiplied = [right.count(num) * num for num in left]
print(sum(counts_multiplied))
