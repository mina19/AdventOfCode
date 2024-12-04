## Pull Data
from pathlib import Path

from get_data import save_data, timeit

save_data(2024, day := 4)
data = Path(f"day{day:02d}.txt").read_text().splitlines()
# data = Path(f"day{day:02d}_sample.txt").read_text().splitlines()

conversion = {"X": 0, "M": 1, "A": 2, "S": 3}
data = [[conversion[letter] for letter in line] for line in data]
rows = len(data)
cols = len(data[0])

directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


# Helper functions
def check_neighbors(col, row):
    neighbors = []

    for dx, dy in directions:
        new_col, new_row = col + dx, row + dy

        if (0 <= new_row < rows) and (0 <= new_col < cols):
            neighbor = data[new_row][new_col]
            neighbors.append((neighbor, (dx, dy)))
    return neighbors


def direction_neighbor(col, row, dx, dy):
    new_col, new_row = col + dx, row + dy
    if (0 <= new_row < rows) and (0 <= new_col < cols):
        return data[new_row][new_col]
    return 0


## Part 1
@timeit
def scan_data():
    count = 0
    for row in range(rows):
        for col in range(cols):
            current = data[row][col]
            if current != 0:
                continue
            neighbors = check_neighbors(col, row)

            # Check to see if all neighbors are valid
            # Only relevant neighbors are where difference was 1
            relevant_directions = [el[1] for el in neighbors if el[0] - current == 1]
            # Check for each of these if the next letter/number is correct
            # It should be a 2
            next_neighbors1 = [
                (dx, dy)
                for dx, dy in relevant_directions
                if direction_neighbor(col + dx, row + dy, dx, dy) == 2
            ]
            if next_neighbors1 != []:
                # Check if the next letter/number is correct
                # It should be a 3
                next_neighbors2 = [
                    (dx, dy)
                    for dx, dy in next_neighbors1
                    if direction_neighbor(col + 2 * dx, row + 2 * dy, dx, dy) == 3
                ]
                if next_neighbors2 != []:
                    count += len(next_neighbors2)

    return count


# hideous solution..... will improve later
output = scan_data()
print(output)


# part 2
@timeit
def scan_data2():
    count = 0
    for row in range(rows):
        for col in range(cols):
            current = data[row][col]
            if current != 2:
                continue
            neighbors = check_neighbors(col, row)

            # Check to see if all neighbors are valid
            # Only relevant neighbors are where difference was 1
            relevant_directions = [el[1] for el in neighbors if el[0] - current == 1]
            # Only interested in diagonals
            good_directions = [(-1, -1), (-1, 1), (1, 1), (1, -1)]
            relevant_directions = set(good_directions).intersection(relevant_directions)

            if (
                len(relevant_directions) >= 2
                and (0 < row < rows - 1)
                and (0 < col < cols - 1)
            ):
                opposite_direction_neighbors = [
                    direction_neighbor(col, row, -dx, -dy)
                    for dx, dy in relevant_directions
                ]
                if opposite_direction_neighbors.count(1) >= 2:
                    # Check the direction neighbor in opposite direction is an M
                    count += 1

    return count


output = scan_data2()
print(output)
