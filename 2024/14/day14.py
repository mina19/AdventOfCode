## Pull Data
import re
from collections import deque
from pathlib import Path

from get_data import save_data, timeit

save_data(2024, day := 14)
data = Path(f"2024/{day}/day{day:02d}.txt").read_text().splitlines()
# In a space which is 101 tiles wide and 103 tiles tall (when viewed from above)
rows = 103
cols = 101

# data = Path(f"2024/{day}/day{day:02d}_sample.txt").read_text().splitlines()
# # In a space which is 11 tiles wide and 7 tiles tall (when viewed from above)
# rows = 7
# cols = 11

pattern = r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)"

robot_data = [re.match(pattern, line) for line in data]
robot_positions = [[int(match[2]), int(match[1])] for match in robot_data]
robot_velocities = [[int(match[4]), int(match[3])] for match in robot_data]


## Part 1
@timeit
def part1(n):
    for _ in range(n):
        for robot_position, robot_velocity in zip(robot_positions, robot_velocities):
            robot_position[0] = (robot_position[0] + robot_velocity[0] + rows) % rows
            robot_position[1] = (robot_position[1] + robot_velocity[1] + cols) % cols

    top_right, top_left, bottom_left, bottom_right = 0, 0, 0, 0
    for robot_position in robot_positions:
        if robot_position[0] < rows // 2 and robot_position[1] < cols // 2:
            top_right += 1
        elif robot_position[0] < rows // 2 and robot_position[1] > cols // 2:
            top_left += 1
        elif robot_position[0] > rows // 2 and robot_position[1] < cols // 2:
            bottom_left += 1
        elif robot_position[0] > rows // 2 and robot_position[1] > cols // 2:
            bottom_right += 1

    result = top_right * top_left * bottom_left * bottom_right

    return result


print(part1(100))

# Re-tare positions
robot_positions = [[int(match[2]), int(match[1])] for match in robot_data]


## Part 2 6620
@timeit
def part2():
    directions = [(0, 1), (0, -1), (-1, 0), (1, 0)]

    def search_for_cluster(start_row, start_col, grid):
        visited = set()
        q = deque()
        q.appendleft((start_row, start_col))
        area = 0

        while q:
            row, col = q.pop()
            if (row, col) in visited:
                continue
            visited.add((row, col))
            area += 1
            for drow, dcol in directions:
                new_row = row + drow
                new_col = col + dcol
                if (
                    0 <= new_row < rows
                    and 0 <= new_col < cols
                    and grid[new_row][new_col] == "#"
                ):
                    q.appendleft((new_row, new_col))
        return area

    i = 0
    keep_searching = True
    while keep_searching:
        grid = [["." for col in range(cols)] for row in range(rows)]

        for robot_position, robot_velocity in zip(robot_positions, robot_velocities):
            robot_position[0] = (robot_position[0] + robot_velocity[0] + rows) % rows
            robot_position[1] = (robot_position[1] + robot_velocity[1] + cols) % cols
            grid[robot_position[0]][robot_position[1]] = "#"

        max_cluster = max(
            search_for_cluster(robot_position[0], robot_position[1], grid)
            for robot_position in robot_positions
        )
        i += 1
        if max_cluster >= 15:
            # Check visual
            for line in grid:
                print("".join(line))
            keep_searching = False

    return i


print(part2())
