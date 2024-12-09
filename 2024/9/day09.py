## Pull Data
from pathlib import Path

from get_data import save_data, timeit

save_data(2024, day := 9)
data = Path(f"2024/{day}/day{day:02d}.txt").read_text().splitlines()[0]
data = Path(f"2024/{day}/day{day:02d}_sample.txt").read_text().splitlines()[0]

# The digits alternate between indicating the length of a file and the length of free space.
diskmap_table = [(int(num), i // 2 if i % 2 == 0 else -1) for i, num in enumerate(data)]


# Part 1
@timeit
def part1():
    while True:
        # Find the first gap
        gap_index = -1
        for i, diskmap_tuple in enumerate(diskmap_table):
            # Entry with a -1 is a gap because it's a free space
            if diskmap_tuple[1] == -1:
                gap_index = i
                break
        if gap_index == -1:
            break
        gap = diskmap_table[gap_index]

        # Second part: Find the next file after the gap
        file_index = -1
        for i in range(gap_index + 1, len(diskmap_table)):
            diskmap_tuple = diskmap_table[i]
            if diskmap_tuple[1] != -1:
                file_index = i
        if file_index == -1:
            break
        file = diskmap_table[file_index]

        if file[0] > gap[0]:  # If file is bigger than gap
            diskmap_table[gap_index] = (gap[0], file[1])
            diskmap_table[file_index] = (file[0] - gap[0], file[1])
            diskmap_table.insert(file_index + 1, (gap[0], -1))
        elif file[0] == gap[0]:  # If file and gap are same size
            diskmap_table[gap_index] = (gap[0], file[1])
            diskmap_table[file_index] = (gap[0], -1)
        else:  # If gap is bigger than file
            diskmap_table[file_index] = (file[0], -1)
            diskmap_table[gap_index] = (file[0], file[1])
            diskmap_table.insert(gap_index + 1, (gap[0] - file[0], -1))
        print([el[0] for el in diskmap_table])

    checksum = 0
    curr_idx = 0
    # To calculate the checksum, add up the result of multiplying
    # each of these blocks' position with the file ID number it contains.
    # The leftmost block is in position 0.
    # If a block contains free space, skip it instead.
    for diskmap_tuple in diskmap_table:
        next_idx = curr_idx + diskmap_tuple[0]
        if diskmap_tuple[1] == -1:
            curr_idx = next_idx
            continue
        while curr_idx < next_idx:
            checksum += curr_idx * diskmap_tuple[1]
            curr_idx += 1

    return checksum


print(part1())


## Part 2
@timeit
def part2():
    pass


part2()
