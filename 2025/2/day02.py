## Pull Data
from pathlib import Path

from get_data import save_data, timeit

save_data(year := 2025, day := 2)
data = Path(f"{year}/{day}/day{day:02d}.txt").read_text()
# data = Path(f"{year}/{day}/day{day:02d}_sample.txt").read_text()


## Part 1
@timeit
def part1():
    # The ranges are separated by commas (,); each range gives its first ID and last ID separated by a dash (-)
    ranges = data.split(",")
    first_id = [int(item.split("-")[0]) for item in ranges]
    last_id = [int(item.split("-")[1]) for item in ranges]
    invalid_ids = []

    def generate_invalid_ids(num1, num2):
        invalid_ids = []
        for length in range(len(str(num1)) // 2, len(str(num2)) // 2 + 1):
            for prefix in range(int(10 ** (length - 1)), int(10**length)):
                s = str(prefix)
                candidate = int(s + s)
                if candidate >= num1 and candidate <= num2:
                    invalid_ids.append(candidate)
        return invalid_ids

    for start, end in zip(first_id, last_id):
        invalid_ids += generate_invalid_ids(start, end)
    return sum(invalid_ids)


print(part1())


## Part 2
@timeit
def part2():
    ranges = data.split(",")
    first_id = [int(item.split("-")[0]) for item in ranges]
    last_id = [int(item.split("-")[1]) for item in ranges]
    invalid_ids = []

    def generate_invalid_ids2(num1, num2):
        invalid_ids = set()
        max_digits = len(str(num2))

        for seq_len in range(1, max_digits // 2 + 1):
            for prefix in range(10 ** (seq_len - 1), 10**seq_len):
                prefix_str = str(prefix)

                for repeat_count in range(2, max_digits // seq_len + 1):
                    candidate_str = prefix_str * repeat_count
                    if len(candidate_str) > max_digits:
                        break

                    candidate = int(candidate_str)
                    if candidate > num2:
                        break
                    if candidate >= num1:
                        invalid_ids.add(candidate)

        return sorted(invalid_ids)

    for start, end in zip(first_id, last_id):
        invalid_ids += generate_invalid_ids2(start, end)
    return sum(invalid_ids)


print(part2())
