## Pull Data
from pathlib import Path

from get_data import save_data, timeit

save_data(2024, day := 9)
data = Path(f"2024/{day}/day{day:02d}.txt").read_text().splitlines()[0]
# data = Path(f"2024/{day}/day{day:02d}_sample.txt").read_text().splitlines()[0]

# The digits alternate between indicating the length of a file and the length of free space.
# If it's a free space, set second number to -1
# If it's a file, set the second number to the file ID
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
            break  # No gaps found so exit while loop
        gap_tuple = diskmap_table[gap_index]

        # Second part: Find the next file after the gap
        file_index = -1
        for i in range(gap_index + 1, len(diskmap_table)):
            diskmap_tuple = diskmap_table[i]
            if diskmap_tuple[1] != -1:
                file_index = i
        if file_index == -1:
            break  # No files after gap so exit while loop
        file_tuple = diskmap_table[file_index]

        gap_length, gap_id = gap_tuple  # gap_id is always -1 by definition of a gap
        file_length, file_id = file_tuple

        if file_length > gap_length:
            diskmap_table[gap_index] = (gap_length, file_id)
            diskmap_table[file_index] = (file_length - gap_length, file_id)
            diskmap_table.insert(file_index + 1, (gap_length, gap_id))
        elif file_length == gap_length:
            diskmap_table[gap_index] = (gap_length, file_id)
            diskmap_table[file_index] = (file_length, gap_id)
        else:
            diskmap_table[gap_index] = (file_length, file_id)
            diskmap_table[file_index] = (file_length, gap_id)
            diskmap_table.insert(gap_index + 1, (gap_length - file_length, gap_id))
        # print([el[1] for el in diskmap_table])

    checksum = 0
    curr_idx = 0
    # To calculate the checksum, add up the result of multiplying
    # each of these blocks' position with the file ID number it contains.
    # The leftmost block is in position 0.
    # If a block contains free space, skip it instead.
    # Example: 009981118882777333...
    # Represented in diskmap_table like this:
    # # [(2, 0), (2, 9), (1, 8), (3, 1), (3, 8), (1, 2), (3, 7), (3, 3), ...]
    for diskmap_tuple in diskmap_table:
        entry_length, entry_id = diskmap_tuple
        next_idx = curr_idx + entry_length
        if entry_id == -1:  # Check if this is a gap
            curr_idx = next_idx
            continue
        while curr_idx < next_idx:
            checksum += curr_idx * entry_id  # This is a file
            curr_idx += 1

    return checksum


print(part1())


## Part 2
@timeit
def part2():
    pass


part2()
