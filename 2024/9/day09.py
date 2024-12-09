## Pull Data
from pathlib import Path

from get_data import save_data, timeit

save_data(2024, day := 9)
data = Path(f"2024/{day}/day{day:02d}.txt").read_text().splitlines()[0]
data = Path(f"2024/{day}/day{day:02d}_sample.txt").read_text().splitlines()[0]

# The digits alternate between indicating the length of a file and the length of free space.
# diskmap_table is a list of tuples where the first number is the length of the entry
# The second number is the file ID if it's a file or -1 if it's a free space/gap
diskmap_table = [(int(num), i // 2 if i % 2 == 0 else -1) for i, num in enumerate(data)]


# Helper function
def compute_checksum(diskmap_table):
    # To calculate the checksum, add up the result of multiplying
    # each of these blocks' position with the file ID number it contains.
    # The leftmost block is in position 0.
    # If a block contains free space, skip it instead.
    # Example block: 009981118882777333...
    # Represented in diskmap_table_copy like this:
    # # [(2, 0), (2, 9), (1, 8), (3, 1), (3, 8), (1, 2), (3, 7), (3, 3), ...]
    # 0 * 0 = 0, 1 * 0 = 0, 2 * 9 = 18, 3 * 9 = 27, 4 * 8 = 32
    checksum = 0
    block_idx = 0
    for diskmap_tuple in diskmap_table:
        entry_length, entry_id = diskmap_tuple
        next_entry_block_idx = block_idx + entry_length
        if entry_id == -1:  # Check if this is a gap
            block_idx = next_entry_block_idx
            continue
        while block_idx < next_entry_block_idx:
            checksum += block_idx * entry_id  # This is a file
            block_idx += 1
    return checksum


# Part 1
@timeit
def part1():
    diskmap_table_copy = diskmap_table.copy()

    while True:
        # Find the first gap
        table_gap_index = -1
        for i, diskmap_tuple in enumerate(diskmap_table_copy):
            # If the tuple has a -1 in the second position, it's a gap
            if diskmap_tuple[1] == -1:
                table_gap_index = i
                break
        gap_tuple = diskmap_table_copy[table_gap_index]

        # Second part: Find the next file after the gap
        table_file_index = -1
        for i in range(table_gap_index + 1, len(diskmap_table_copy)):
            # Keep iterating until finding the last file after the gap
            diskmap_tuple = diskmap_table_copy[i]
            if diskmap_tuple[1] != -1:
                table_file_index = i
        if table_file_index == -1:
            break  # No files after gap so exit while loop
        file_tuple = diskmap_table_copy[table_file_index]

        gap_length, gap_id = gap_tuple  # gap_id is always -1 by definition of a gap
        file_length, file_id = file_tuple

        # Rearrange the diskmap_table_copy
        if file_length > gap_length:
            # Since the file length is bigger than the gap length,
            # move part of the file to the gap
            diskmap_table_copy[table_gap_index] = (gap_length, file_id)
            # The remaining part of the file still remains where it was
            diskmap_table_copy[table_file_index] = (file_length - gap_length, file_id)
            # Because the file length was larger than the gap length, we need to track
            # the original gap in the diskmap_table_copy
            diskmap_table_copy.insert(table_file_index + 1, (gap_length, gap_id))
        elif file_length == gap_length:
            # Swap the file and the gap
            diskmap_table_copy[table_gap_index] = (file_length, file_id)
            diskmap_table_copy[table_file_index] = (file_length, gap_id)
        else:
            # Move the file to the gap
            diskmap_table_copy[table_gap_index] = (file_length, file_id)
            diskmap_table_copy[table_file_index] = (file_length, gap_id)
            # Because the gap length was larger than the file length, we need to track
            # the remaining original gap in the diskmap_table_copy
            diskmap_table_copy.insert(
                table_gap_index + 1, (gap_length - file_length, gap_id)
            )

    return compute_checksum(diskmap_table_copy)


print(part1())


## Part 2
@timeit
def part2():
    # Iterates through files from middle to start
    # For each file, finds a gap earlier in the table that's large enough
    # If found, moves the file to that gap
    # If the gap is larger than needed, split it into used and remaining gap
    # Merges adjacent gaps
    # Repeats until no more moves are possible
    diskmap_table_copy = diskmap_table.copy()

    stop = False
    while not stop:
        stop = True
        # Length of original data will not change but length of diskmap_table_copy will
        for idx in range(len(data) // 2, -1, -1):
            # Find the next file
            table_file_index = -1
            for i, diskmap_tuple in enumerate(diskmap_table_copy):
                # Check if the file ID is the one we're looking for
                if diskmap_tuple[1] == idx:
                    # print(f"File {idx} found at index {i}")
                    table_file_index = i
            if table_file_index == -1:
                continue
            file_length, file_id = diskmap_table_copy[table_file_index]

            # Find the first gap that satisfies length requirement
            table_gap_index = -1
            for i in range(table_file_index):
                diskmap_tuple = diskmap_table_copy[i]
                if diskmap_tuple[1] == -1 and diskmap_tuple[0] >= file_length:
                    table_gap_index = i
                    break
            if table_gap_index == -1:
                continue
            gap_length, gap_id = diskmap_table_copy[
                table_gap_index
            ]  # gap_id is always -1 by definition of a gap
            stop = False

            # Rearrange the diskmap_table_copy
            if file_length == gap_length:
                # Swap the file and the gap
                diskmap_table_copy[table_gap_index] = (file_length, file_id)
                diskmap_table_copy[table_file_index] = (file_length, gap_id)
            else:
                # Move the file to the gap
                diskmap_table_copy[table_gap_index] = (file_length, file_id)
                diskmap_table_copy[table_file_index] = (file_length, gap_id)
                # Because the gap length was larger than the file length, we need to track
                # the remaining original gap in the diskmap_table_copy
                diskmap_table_copy.insert(
                    table_gap_index + 1, (gap_length - file_length, gap_id)
                )

            i = 0
            while i < len(diskmap_table_copy) - 1:
                diskmap_tuple = diskmap_table_copy[i]
                next_diskmap_tuple = diskmap_table_copy[i + 1]
                # Merge adjacent gaps
                if diskmap_tuple[1] == -1 and next_diskmap_tuple[1] == -1:
                    diskmap_table_copy[i] = (
                        diskmap_tuple[0] + next_diskmap_tuple[0],
                        -1,
                    )
                    del diskmap_table_copy[i + 1]
                else:
                    i += 1

        stop = True

    return compute_checksum(diskmap_table_copy)


print(part2())
