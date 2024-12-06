## Pull Data
from pathlib import Path
from collections import defaultdict
import copy

from get_data import save_data, timeit

save_data(2024, day := 6)
data = Path(f"day{day:02d}.txt").read_text().splitlines()
# data = Path(f"2024/day{day:02d}_sample.txt").read_text().splitlines()

# Hash the data. If we hit boundary return a !
data_dict = defaultdict(
    lambda: defaultdict(lambda: "!"),  # Invalid row
    enumerate(
        defaultdict((lambda: "!"), enumerate(line)) for line in data
    ),  # Invalid column,
)

# Shape of data
rows = len(data)
cols = len(data[0])


## Part 1
@timeit
def part1():
    # Nested dictionary requires deepcopy
    data_dict_copy = copy.deepcopy(data_dict)

    # Lazy way to find the coordinates of ^
    i = 0
    j = 0
    for row in range(rows):
        for col in range(cols):
            if data_dict_copy[row][col] == "^":
                i = row
                j = col

    # Begin traversing the grid/dictionary
    result = 0
    current = (-1, 0)  # Starting direction North
    while data_dict_copy[i][j] != "!":  # Continue until hitting boundary
        # Mark current position as visited
        if data_dict_copy[i][j] != "X":
            data_dict_copy[i][j] = "X"
            result += 1

        # If hitting a wall (#), rotate direction right
        if data_dict_copy[i + current[0]][j + current[1]] == "#":
            # Direction order: [(-1, 0), (0, 1), (1, 0), (0, -1)]
            # (-1, 0) -> (0, 1)   # North -> East
            # (0, 1) -> (1, 0)    # East -> South
            # (1, 0) -> (0, -1)   # South -> West
            # (0, -1) -> (-1, 0)  # West -> North
            current = (current[1], -current[0])
        else:
            # Move in current direction
            i += current[0]
            j += current[1]
    return result


print(part1())


## Part 2
@timeit
def part2():
    # Nested dictionary requires deepcopy
    data_dict_copy = copy.deepcopy(data_dict)

    # Lazy way to find the coordinates of ^
    start_i = 0
    start_j = 0
    for row in range(rows):
        for col in range(cols):
            if data_dict_copy[row][col] == "^":
                start_i = row
                start_j = col

    valid_obstruction_count = 0
    for obstruction_i in range(rows):
        for obstruction_j in range(cols):
            # Start again from ^
            i = start_i
            j = start_j

            if data_dict_copy[obstruction_i][obstruction_j] != ".":
                continue

            # Turn spot into an obstruction
            data_dict_copy[obstruction_i][obstruction_j] = "#"

            # Count number of steps for this obstruction
            steps = 0
            current = (-1, 0)  # Starting direction North
            while data_dict_copy[i][j] != "!":
                steps += 1
                if data_dict_copy[i + current[0]][j + current[1]] == "#":
                    # Hit a wall so update direction
                    current = (current[1], -current[0])
                else:
                    # Move in current direction
                    i += current[0]
                    j += current[1]

                # Shouldn't have to step more than area of grid
                if steps >= rows * cols:
                    valid_obstruction_count += 1
                    break

            # Turn spot back into a .
            data_dict_copy[obstruction_i][obstruction_j] = "."
    return valid_obstruction_count


print(part2())
