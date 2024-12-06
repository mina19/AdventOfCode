## Pull Data
from pathlib import Path
import numpy as np

from get_data import save_data, timeit

save_data(2024, day := 6)
data = Path(f"day{day:02d}.txt").read_text().splitlines()
data = Path(f"2024/day{day:02d}_sample.txt").read_text().splitlines()
conversion = {".": 0, "#": 1, "^": 2}
data = np.array([[conversion[el] for el in line] for line in data])

rows, cols = data.shape
directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]

## Part 1


@timeit
def part1():
    # Copy original data
    copy = np.copy(data)

    # Set up tracking
    visited_coords = set()

    # Starting coordinates
    coordinates = np.argwhere(copy == 2)
    start_row = int(coordinates[0][0])
    start_col = int(coordinates[0][1])
    visited_coords.add((start_row, start_col))

    def traverse_direction(direction, starting_coordinates):
        if direction == (1, 0):
            for i in range(starting_coordinates[0], -1, -1):
                if copy[i, starting_coordinates[1]] != 1:
                    visited_coords.add((i, starting_coordinates[1]))
                    if i == 0:
                        return 0, 0, True
                else:
                    return i + 1, starting_coordinates[1], i == 0
        elif direction == (0, 1):
            for j in range(starting_coordinates[1], cols):
                if copy[starting_coordinates[0], j] != 1:
                    visited_coords.add((starting_coordinates[0], j))
                else:
                    return starting_coordinates[0], j - 1, j == cols
        elif direction == (-1, 0):
            for i in range(starting_coordinates[0], rows):
                if copy[i, starting_coordinates[1]] != 1:
                    visited_coords.add((i, starting_coordinates[1]))
                else:
                    return i - 1, starting_coordinates[1], i == rows
        else:
            for j in range(starting_coordinates[1], -1, -1):
                if copy[starting_coordinates[0], j] != 1:
                    visited_coords.add((starting_coordinates[0], j))
                else:
                    return starting_coordinates[0], j + 1, j == -1

    def loop_all_directions(start_row, start_col):
        for direction in directions:
            if traverse_direction(direction, (start_row, start_col)):
                start_row, start_col, exit = traverse_direction(
                    direction, (start_row, start_col)
                )
        return start_row, start_col, exit

    i = 0
    while i < 5:
        if loop_all_directions(start_row, start_col):
            start_row, start_col, exit = loop_all_directions(start_row, start_col)
        else:
            exit = True
        i += 1

    return len(visited_coords)


print(part1())
## Part 2


@timeit
def part2():
    pass


part2()
