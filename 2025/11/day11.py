## Pull Data
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

    return len(paths)


def part2_memoized(start_device, end_device):
    start_device = next(device for device in devices if device == start_device)

    memo = {}

    # Slow. Do not do.
    def count_paths(current_device, visited_tuple):
        # Count distinct paths from this device to "out"
        if (current_device, visited_tuple) in memo:
            return memo[(current_device, visited_tuple)]

        # Base case: reached the end
        if current_device == end_device:
            return 1

        # Explore all future devices
        total_paths = 0
        for future_device in data_dict[current_device]:
            if future_device not in visited_tuple:
                # Add current device to visited set
                new_visited = visited_tuple + (future_device,)
                total_paths += count_paths(future_device, new_visited)

        memo[(current_device, visited_tuple)] = total_paths
        return total_paths

    # Fast. But does not handle required devices.
    def count_paths_dag(current_device):
        # Only works if there are no cycles in the graph
        if current_device in memo:
            return memo[current_device]

        # Base case
        if current_device == end_device:
            return 1

        # Sum paths through all neighbors
        total_paths = sum(
            count_paths_dag(next_device) for next_device in data_dict[current_device]
        )

        memo[current_device] = total_paths
        return total_paths

    def count_paths_through_required(
        current_device: str, required_remaining: frozenset
    ):
        if (current_device, required_remaining) in memo:
            return memo[(current_device, required_remaining)]

        # Base case
        if current_device == end_device:
            return 1 if len(required_remaining) == 0 else 0

        # Update required devices if we just visited one
        new_required = (
            required_remaining - {current_device}
            if current_device in required_remaining
            else required_remaining
        )

        # Sum paths through all neighbors
        total_paths = sum(
            count_paths_through_required(next_device, new_required)
            for next_device in data_dict[current_device]
        )

        memo[(current_device, new_required)] = total_paths
        return total_paths

    return count_paths_through_required(start_device, frozenset(["fft", "dac"]))


print(part2_memoized("svr", "out"))
