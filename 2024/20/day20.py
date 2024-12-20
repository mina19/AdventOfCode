## Pull Data
from collections import defaultdict, deque
from functools import cache
from pathlib import Path

from get_data import save_data, timeit

save_data(2024, day := 20)
data = Path(f"2024/{day}/day{day:02d}.txt").read_text().splitlines()
# data = Path(f"2024/{day}/day{day:02d}_sample.txt").read_text().splitlines()

rows = len(data)
cols = len(data[0])

data_dict = defaultdict(
    lambda: defaultdict(lambda: "!"),
    enumerate(defaultdict((lambda: "!"), enumerate(line)) for line in data),
)
directions = [(0, 1), (0, -1), (-1, 0), (1, 0)]

for row in range(rows):
    for col in range(cols):
        if data_dict[row][col] == "S":
            start_row, start_col = row, col
        elif data_dict[row][col] == "E":
            end_row, end_col = row, col


# Helper functions
# Needed for Part 2
def get_grid_times(target_row, target_col, grid_times: dict = None):
    if grid_times is None:
        grid_times = {}

    q = deque()
    q.append((0, target_row, target_col))

    while q:
        time, row, col = q.popleft()
        if (row, col) in grid_times:
            continue

        if data_dict[row][col] not in {"#", "!"}:
            grid_times[(row, col)] = time
            for drow, dcol in directions:
                q.append((time + 1, row + drow, col + dcol))

    return grid_times


@cache
def search_nocheat(start_row, start_col, target_row, target_col):
    visited = set()

    q = deque()
    q.append((0, start_row, start_col))

    while q:
        nocheat_time, row, col = q.popleft()
        if (row, col) in visited:
            continue

        visited.add((row, col))
        if row == target_row and col == target_col:
            return nocheat_time
        else:
            for drow, dcol in directions:
                char = data_dict[row + drow][col + dcol]
                if (char != "#" and char != "!") or (
                    row + drow == target_row and col + dcol == target_col
                ):
                    q.append((nocheat_time + 1, row + drow, col + dcol))


## Part 1
@timeit
def part1():
    nocheat_time = search_nocheat(start_row, start_col, end_row, end_col)

    result = 0
    for cheat_row in range(rows):
        for cheat_col in range(cols):
            for drow, dcol in directions:
                if data_dict[cheat_row][cheat_col] != "#":
                    continue
                if data_dict[cheat_row + drow][cheat_col + dcol] in {".", "E"}:
                    cheat_time = (
                        (
                            search_nocheat(start_row, start_col, cheat_row, cheat_col)
                            + 1
                            + search_nocheat(
                                cheat_row + drow,
                                cheat_col + dcol,
                                end_row,
                                end_col,
                            )
                        )
                        if (cheat_row, cheat_col) != (end_row, end_col)
                        else nocheat_time
                    )
                    if cheat_time <= nocheat_time - 100:
                        result += 1

    return result


# print(part1())


## Part 2
@timeit
def part2():
    nocheat_times_from_start = get_grid_times(start_row, start_col)
    nocheat_times_to_end = get_grid_times(end_row, end_col)

    nocheat_time = nocheat_times_from_start[(end_row, end_col)]

    result = 0
    for row1 in range(rows):
        for col1 in range(cols):
            if data_dict[row1][col1] in {"#", "!"}:
                continue
            for row2 in range(rows):
                for col2 in range(cols):
                    if data_dict[row2][col2] in {"#", "!"}:
                        continue
                    cheat_dist = abs(row2 - row1) + abs(col2 - col1)
                    if cheat_dist > 20:
                        continue
                    cheat_time = (
                        nocheat_times_from_start[(row1, col1)]
                        + cheat_dist
                        + nocheat_times_to_end[(row2, col2)]
                    )
                    if cheat_time <= nocheat_time - 100:
                        result += 1

    return result


print(part2())
