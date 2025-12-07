## Pull Data
from collections import defaultdict
from pathlib import Path

# from get_data import save_data, timeit

# save_data(year := 2025, day := 7)
year = 2025
day = 7
lines = Path(f"{year}/{day}/day{day:02d}.txt").read_text().splitlines()
# lines = Path(f"{year}/{day}/day{day:02d}_sample.txt").read_text().splitlines()

# Shape of data
rows = len(lines)
cols = len(lines[0])

# Hash the data. If we hit a boundary return !
data_dict = defaultdict(
    lambda: defaultdict(lambda: "!"),  # Invalid row
    enumerate(
        defaultdict((lambda: "!"), enumerate(line)) for line in lines
    ),  # Invalid column
)


## Part 1
# @timeit
def part1():
    start_col = None
    for col in range(cols):
        if data_dict[0][col] == 'S':
            start_col = col
    
    beam_cols = {start_col}
    count = 0
    
    for row in range(rows):
        new_beam_cols = set()
        for beam_col in beam_cols:
            if data_dict[row][beam_col] == "^":
                count += 1
                if data_dict[row+1][beam_col - 1] != "!":
                    new_beam_cols.add(beam_col - 1)
                if data_dict[row+1][beam_col + 1] != "!":
                    new_beam_cols.add(beam_col + 1)
            else:
                new_beam_cols.add(beam_col)
        
        beam_cols = new_beam_cols
    
    return count



print(part1())


## Part 2
# @timeit
def part2():
    pass


part2()
