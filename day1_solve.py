### Part 1 ###
day1lines = [line.rstrip() for line in open('day1_input.txt')]
# day1lines = [line.rstrip() for line in open('day1_sample.txt')]

nums_list = []
for line in day1lines:
    nums_list.append([int(x) for x in [*line] if x.isdigit()])

sum_calibration_vals = sum([nums[0] for nums in nums_list])*10 + sum([nums[-1] for nums in nums_list])
print(sum_calibration_vals)
