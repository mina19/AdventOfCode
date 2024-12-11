## Pull Data
from pathlib import Path
from collections import Counter

from get_data import save_data, timeit

save_data(2024, day := 11)
data = Path(f"2024/{day}/day{day:02d}.txt").read_text().splitlines()
# data = Path(f"2024/{day}/day{day:02d}_sample.txt").read_text().splitlines()


## Part 1
@timeit
def part1(n):
    stones = [int(num) for num in data[0].split()]
    for i in range(n):
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
    stones = [int(num) for num in data[0].split()]
    stones = Counter(stones)

    for i in range(n):
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
