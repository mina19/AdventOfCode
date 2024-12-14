## Pull Data
from pathlib import Path

from get_data import save_data, timeit
import re

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


## Part 2
@timeit
def part2():
    pass


part2()
