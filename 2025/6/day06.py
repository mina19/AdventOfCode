## Pull Data
import math
from collections import defaultdict
from pathlib import Path

from get_data import save_data, timeit

save_data(year := 2025, day := 6)
data = Path(f"{year}/{day}/day{day:02d}.txt").read_text()
data = Path(f"{year}/{day}/day{day:02d}_sample.txt").read_text()


## Part 1
@timeit
def part1():
    nums = defaultdict(list)
    result = 0
    
    for line in data.splitlines():
        parts = line.split()
        
        for i, part in enumerate(parts):
            if part == "*":
                result += math.prod(nums[i])
            elif part == "+":
                result += sum(nums[i])
            else:
                nums[i].append(int(part))
    
    return result

print(part1())


## Part 2
@timeit
def part2():
    lines = data.splitlines()
    last_line = lines[-1]
    
    # Find column positions where operators/numbers appear
    offsets = [i for i, c in enumerate(last_line) if c != " "]
    
    # Calculate width of each column
    widths = [offsets[i + 1] - offsets[i] - 1 for i in range(len(offsets) - 1)]
    widths.append(len(last_line) - offsets[-1])
    
    # Track what the numbers for each operation should be
    nums = [[""] * width for width in widths]
    
    result = 0
    for line in lines:
        for i, offset in enumerate(offsets):
            char = line[offset]
            
            if char == "*":
                result += math.prod(int(x) for x in nums[i])
            elif char == "+":
                result += sum(int(x) for x in nums[i])
            else:
                # Accumulate multi-character numbers across columns
                for j in range(widths[i]):
                    if line[offset + j] != " ":
                        nums[i][j] += line[offset + j]
    
    return result


print(part2())