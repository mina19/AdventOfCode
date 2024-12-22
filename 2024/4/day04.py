## Pull Data
from pathlib import Path

import numpy as np

from get_data import save_data, timeit

save_data(2024, day := 4)

# Read in data
data = Path(f"2024/4/day{day:02d}.txt").read_text().splitlines()
# data = Path(f"2024/4day{day:02d}_sample.txt").read_text().splitlines()

# Convert data to numbers for easier analysis
conversion = {"X": 0, "M": 1, "A": 2, "S": 3}
data = np.array([[conversion[letter] for letter in line] for line in data])
rows, cols = data.shape

directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
diagonal_directions = [(-1, -1), (-1, 1), (1, 1), (1, -1)]


# Helper functions
def check_neighbors(col, row):
    neighbors = []

    for dx, dy in directions:
        new_col, new_row = col + dx, row + dy

        if (0 <= new_row < rows) and (0 <= new_col < cols):
            neighbor = data[new_row, new_col]
            neighbors.append((neighbor, (dx, dy)))
    return neighbors


def direction_neighbor(col, row, dx, dy):
    new_col, new_row = col + dx, row + dy
    if (0 <= new_row < rows) and (0 <= new_col < cols):
        return data[new_row, new_col]
    return -1


## Part 1
@timeit
def part1():
    count = 0
    for row in range(rows):
        for col in range(cols):
            current = data[row, col]
            if current != 0:
                continue
            neighbors = check_neighbors(col, row)

            # Only relevant neighbors are where difference is 1
            relevant_directions = [el[1] for el in neighbors if el[0] - current == 1]
            # Check for each of these if the next letter/number is correct
            # It should be a 2 / letter A
            next_neighbors1 = [
                (dx, dy)
                for dx, dy in relevant_directions
                if direction_neighbor(col + dx, row + dy, dx, dy) == 2
            ]
            if next_neighbors1 != []:
                # Check if the next letter/number is correct
                # It should be a 3 / letter S
                next_neighbors2 = [
                    (dx, dy)
                    for dx, dy in next_neighbors1
                    if direction_neighbor(col + 2 * dx, row + 2 * dy, dx, dy) == 3
                ]
                if next_neighbors2 != []:
                    count += len(next_neighbors2)

    return count


# Original solution
output = part1()
print(output)


# Different way to do Part 1
## Part 1
@timeit
def part1_b():
    count = 0
    for row in range(rows):
        for col in range(cols):
            current = data[row, col]
            if current != 0:
                continue

            for dx, dy in directions:
                current = ""
                for step in range(4):
                    current += str(direction_neighbor(col, row, dx * step, dy * step))

                if current == "0123":
                    count += 1

    return count


print(part1_b())


# Part 2
@timeit
def part2():
    count = 0
    for row in range(rows):
        for col in range(cols):
            current = data[row, col]
            if current != 2:  # Check with the letter A
                continue
            neighbors = check_neighbors(col, row)

            # Only relevant neighbors are where difference is 1
            relevant_directions = [el[1] for el in neighbors if el[0] - current == 1]
            # Only interested in diagonals
            relevant_directions = set(diagonal_directions).intersection(
                relevant_directions
            )

            if len(relevant_directions) >= 2:
                # Check the direction neighbor in opposite direction is a 1 / letter M and that there are 2 of them
                opposite_direction_neighbors = [
                    direction_neighbor(col, row, -dx, -dy)
                    for dx, dy in relevant_directions
                ]
                if opposite_direction_neighbors.count(1) == 2:
                    count += 1

    return count


output = part2()
print(output)
