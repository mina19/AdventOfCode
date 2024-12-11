## Pull Data
from pathlib import Path
from collections import Counter

from get_data import save_data, timeit

save_data(2024, day := 11)
data = Path(f"2024/{day}/day{day:02d}.txt").read_text().splitlines()
data = Path(f"2024/{day}/day{day:02d}_sample.txt").read_text().splitlines()


## Part 1
@timeit
def part1(n):
    # [253000, 1, 7]
    # [253, 0, 2024, 14168]
    # [512072, 1, 20, 24, 28676032]
    # [512, 72, 2024, 2, 0, 2, 4, 2867, 6032]
    # [1036288, 7, 2, 20, 24, 4048, 1, 4048, 8096, 28, 67, 60, 32]
    stones = [int(num) for num in data[0].split()]
    for i in range(n):
        # Create a new list with all stones, including duplicates
        # Probably won't scale...
        new_stones = []
        for stone in stones:
            stone_string = str(stone)
            stone_length = len(stone_string)
            if stone == 0:
                new_stones.append(1)
            elif stone_length % 2 == 0:
                new_stones.append(int(stone_string[: (stone_length // 2)]))
                new_stones.append(int(stone_string[(stone_length // 2) :]))
            else:
                new_stones.append(stone * 2024)
        stones = new_stones

    return len(stones)


print(part1(25))


## Part 2
@timeit
def part2(n):
    # Counter({253000: 1, 1: 1, 7: 1})
    # Counter({253: 1, 0: 1, 2024: 1, 14168: 1})
    # Counter({512072: 1, 1: 1, 20: 1, 24: 1, 28676032: 1})
    # Counter({2: 2, 512: 1, 72: 1, 2024: 1, 0: 1, 4: 1, 2867: 1, 6032: 1})
    # Counter({4048: 2, 1036288: 1, 7: 1, 2: 1, 20: 1, 24: 1, 1: 1, 8096: 1, 28: 1, 67: 1, 60: 1, 32: 1})
    stones = [int(num) for num in data[0].split()]
    stones = Counter(stones)

    for i in range(n):
        # Only store unique values with their counts
        # Should scale
        new_stones = Counter()
        for stone, stone_count in stones.items():
            stone_string = str(stone)
            stone_length = len(stone_string)
            if stone == 0:
                new_stones[1] += stone_count
            elif stone_length % 2 == 0:
                new_stones[int(stone_string[: (stone_length // 2)])] += stone_count
                new_stones[int(stone_string[(stone_length // 2) :])] += stone_count
            else:
                new_stones[stone * 2024] += stone_count
        stones = new_stones

    # Count up values in most common
    result = 0
    for stone, stone_count in new_stones.most_common():
        result += stone_count

    return result


print(part2(75))
