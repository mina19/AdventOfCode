## Pull Data
from get_data import save_data

save_data(2024, 1)

## Part 1
day1lines = [line.rstrip() for line in open("day01.txt")]
list1 = [int(nums.split("   ")[0]) for nums in day1lines]
list2 = [int(nums.split("   ")[1]) for nums in day1lines]

list1.sort()
list2.sort()

diffs = [abs(list2[i] - list1[i]) for i in range(len(list1))]

print(sum(diffs))


## Part 2
counts_multiplied = [list2.count(num) * num for num in list1]

print(sum(counts_multiplied))
