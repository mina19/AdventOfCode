## Pull Data
from pathlib import Path

import numpy as np

# from get_data import save_data, timeit

# save_data(year := 2025, day := 1)
day = 12
year = 2025
data = Path(f"{year}/{day}/day{day:02d}.txt").read_text()
data = Path(f"{year}/{day}/day{day:02d}_sample.txt").read_text()

# Put in additional \n manually in txt files for easier parsing
present_shapes_data = data.split('\n\n\n')[0]
requirements_data = data.split('\n\n\n')[1]

present_shapes = {}

present_blocks = present_shapes_data.strip().split('\n\n')

for block in present_blocks:
    lines = block.strip().split('\n')
    present_id = int(lines[0].rstrip(':'))
    grid_rows = lines[1:]
    
    grid = []
    for row in grid_rows:
        grid.append([1 if char == '#' else 0 for char in row])
    
    present_shapes[present_id] = np.array(grid)

requirements = []
    
for line in requirements_data.strip().split('\n'):
    grid_part, counts_part = line.split(': ')
    
    width, height = map(int, grid_part.split('x'))
    grid_size = (width, height)
    
    present_counts = {
        present_id: count 
        for present_id, count in enumerate(map(int, counts_part.split()))
    }
    
    requirements.append({
        'grid_size': grid_size,
        'present_counts': present_counts
    })

## Part 1
# @timeit
def part1():
    pass


part1()


## Part 2
# @timeit
def part2():
    pass


part2()
