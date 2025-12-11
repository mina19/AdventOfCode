## Pull Data
from functools import lru_cache
from pathlib import Path

from get_data import save_data, timeit

save_data(year := 2025, day := 11)
data = Path(f"{year}/{day}/day{day:02d}.txt").read_text().splitlines()
# data = Path(f"{year}/{day}/day{day:02d}_sample.txt").read_text().splitlines()

devices = [line.split(":")[0] for line in data]
outputs = [line.split(":")[1].split(" ")[1:] for line in data]
data_dict = dict(zip(devices, outputs))


## Part 1
@timeit
def part1():
    start_device = next(device for device in devices if device == "you")
    paths = [[start_device]]
    all_paths = []

    while paths:
        new_paths = []
        for path in paths:
            last_device = path[-1]
            if last_device == "out":
                all_paths.append(path)
                continue
            for future_device in data_dict[last_device]:
                if future_device not in path:
                    new_paths.append(path + [future_device])
        paths = new_paths

    return len(all_paths)


# print(part1())


## Part 2
@timeit
def part2_did_not_scale(start_device, required_devices):
    start_device = next(device for device in devices if device == start_device)
    paths = [[start_device]]
    all_paths = []

    while paths:
        new_paths = []
        for path in paths:
            last_device = path[-1]
            if last_device == "out":
                all_paths.append(path)
                continue
            for future_device in data_dict[last_device]:
                if future_device not in path:
                    new_paths.append(path + [future_device])
        paths = new_paths

    valid_paths = [
        path for path in all_paths if all(device in path for device in required_devices)
    ]

    return len(valid_paths)


def solve(start_device, required_devices):
    required_devices = tuple(required_devices)

    @lru_cache(maxsize=None)
    def dfs(current, visited):
        visited_set = set(visited)
        if current == "out":
            if all(device in visited_set for device in required_devices):
                return 1
            return 0
        count = 0
        for next_device in data_dict[current]:
            if next_device not in visited_set:
                count += dfs(next_device, tuple(list(visited_set) + [next_device]))
        return count

    return dfs(start_device, (start_device,))


print(solve("dac", "fft"))
print(solve("fft", "dac"))
