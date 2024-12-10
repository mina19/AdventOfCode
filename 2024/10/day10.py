## Pull Data
from collections import defaultdict, deque
from pathlib import Path

from get_data import save_data, timeit

save_data(2024, day := 10)
data = Path(f"2024/{day}/day{day:02d}.txt").read_text().splitlines()
data = Path(f"2024/{day}/day{day:02d}_sample.txt").read_text().splitlines()

data_dict = defaultdict(
    lambda: defaultdict(lambda: "!"),
    enumerate(defaultdict((lambda: "!"), enumerate(line)) for line in data),
)

rows = len(data)
cols = len(data[0])

directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]


def trailhead_count(distinct=False):
    result = 0
    for row in range(rows):
        for col in range(cols):
            if data_dict[row][col] == "0":
                # States will track the current positions starting from 0
                states = deque()
                states.append((row, col))

                if not distinct:  # Part 1s
                    visited = set()
                while states:
                    current_row, current_col = states.popleft()
                    current_val = int(data_dict[current_row][current_col])
                    if not distinct:  # Part 1
                        if (current_row, current_col) in visited:
                            continue
                        # Haven't seen this position before
                        visited.add((current_row, current_col))

                    if data_dict[current_row][current_col] == "9":
                        # Reached a position of 9-height
                        result += 1

                    elif data_dict[current_row][current_col] != "!":
                        for drow, dcol in directions:
                            # Check if next position is valid
                            if data_dict[current_row + drow][current_col + dcol] == str(
                                1 + current_val
                            ):
                                states.append((current_row + drow, current_col + dcol))

    return result


## Part 1
@timeit
def part1():
    # Want to count only the unique 9-height positions we get to
    return trailhead_count(distinct=False)


print(part1())


## Part 2
@timeit
def part2():
    return trailhead_count(distinct=True)


print(part2())
