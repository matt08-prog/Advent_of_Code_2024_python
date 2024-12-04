import re
lines = []
# input_file_name = "test_input_1.txt"
input_file_name = "real_input.txt"

with open(input_file_name) as file:
    for line in file:
        lines.append(line)
print(lines)

mul_results_sum = 0

for line in lines:
    multiply_instructions = re.findall(r"mul\([0-9]+,[0-9]+\)", line)
    print(multiply_instructions)
    for instruction in multiply_instructions:
        nums = [int(i) for i in re.findall(r"[0-9]+", instruction)]
        product = nums[0] * nums[1]
        mul_results_sum += product
        print(nums)
        print(product)
# for floor_index in range(len(floors)):
#     floor = floors[floor_index]
#     level_dir = int(floor[1] - floor[0] > 0) # 0 for down, 1 for up
#     num_safe_floors += 1
#     for level in range(len(floor) - 1):
#         difference = floor[level+1] - floor[level]
#         new_level_dir = int(difference > 0) # 0 for down, 1 for up

#         if abs(difference) < 1 or abs(difference) > 3 or new_level_dir != level_dir:
#             num_safe_floors -= 1
#             break

print(mul_results_sum) # answer: 160672468