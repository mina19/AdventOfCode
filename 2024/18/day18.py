## Pull Data
from collections import defaultdict, deque
from heapq import heappop, heappush
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
grid = defaultdict((lambda: defaultdict(lambda: ".")))


## Part 1
@timeit
def part1(corruption_length=corruption_length):
    def add_corrupted_data(corruption_length):
        corrupted_data = [
            (int(x.split(",")[0]), int(x.split(",")[1]))
            for x in data[:corruption_length]
        ]

        # Add corrupted data
        for row, col in corrupted_data:
            grid[row][col] = "#"

    add_corrupted_data(corruption_length)

    visited = set()
    q = deque()
    q.appendleft((0, 0, 0))  # Track cost, row, col
    best_cost = float("inf")

    while q:
        cost, row, col = q.pop()
        if (row, col) in visited:
            continue

        visited.add((row, col))
        if grid[row][col] == "#" or row < 0 or row >= rows or col < 0 or col >= cols:
            continue
        if row == rows - 1 and col == cols - 1:
            best_cost = min(cost, best_cost)
        for drow, dcol in directions:
            q.appendleft((cost + 1, row + drow, col + dcol))

    return best_cost


@timeit
def part1_heap(corruption_length=corruption_length):
    def add_corrupted_data(corruption_length):
        corrupted_data = [
            (int(x.split(",")[0]), int(x.split(",")[1]))
            for x in data[:corruption_length]
        ]

        # Add corrupted data
        for row, col in corrupted_data:
            grid[row][col] = "#"

    add_corrupted_data(corruption_length)

    priority_queue = [(0, 0, 0)]  # Track cost, row, col
    visited = set()
    best_cost = float("inf")

    while priority_queue:
        cost, row, col = heappop(priority_queue)
        if (row, col) in visited:
            continue

        visited.add((row, col))
        if grid[row][col] == "#" or row < 0 or row >= rows or col < 0 or col >= cols:
            continue
        if row == rows - 1 and col == cols - 1:
            best_cost = min(cost, best_cost)
        for drow, dcol in directions:
            heappush(priority_queue, (cost + 1, row + drow, col + dcol))

    return best_cost


print(part1())

print(part1_heap())


## Part 2
#  This is sub-optimal, but it works. Will improve
@timeit
def part2():
    for corruption_length in range(len(data)):
        if part1(corruption_length) == float("inf"):
            break

    return data[corruption_length - 1]


print(part2())
