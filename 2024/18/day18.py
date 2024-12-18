## Pull Data
from collections import defaultdict, deque
from pathlib import Path

from get_data import save_data, timeit

save_data(2024, day := 18)
data = Path(f"2024/{day}/day{day:02d}.txt").read_text().splitlines()
rows, cols = 71, 71
corruption_length = 1024

# data = Path(f"2024/{day}/day{day:02d}_sample.txt").read_text().splitlines()
# rows, cols = 7, 7
# corruption_length = 12

directions = [(0, 1), (0, -1), (-1, 0), (1, 0)]
data_dict = defaultdict((lambda: defaultdict(lambda: ".")))

corrupted_data = [
    (int(x.split(",")[0]), int(x.split(",")[1])) for x in data[:corruption_length]
]

# Add corrupted data
for row, col in corrupted_data:
    data_dict[row][col] = "#"


## Part 1
@timeit
def part1():
    visited = set()
    q = deque()
    q.appendleft((0, 0, 0))  # Track cost, row, col
    best_cost = float("inf")

    while q:
        cost, row, col = q.pop()
        if (row, col) in visited:
            continue

        visited.add((row, col))
        if (
            data_dict[row][col] == "#"
            or row < 0
            or row >= rows
            or col < 0
            or col >= cols
        ):
            continue
        if row == rows - 1 and col == cols - 1:
            best_cost = min(cost, best_cost)
        for drow, dcol in directions:
            q.appendleft((cost + 1, row + drow, col + dcol))

    return best_cost


print(part1())


## Part 2
@timeit
def part2():
    pass


part2()