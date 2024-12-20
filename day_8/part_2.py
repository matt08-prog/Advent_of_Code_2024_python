import math
import re
lines = []
input_file_name = "test_input_1.txt"
input_file_name = "real_input.txt"

with open(input_file_name) as file:
    for line in file:
        lines.append(line.strip())
num_cols = len(lines[0])
num_rows = len(lines)

antenna_locs = []

for line_index, row in enumerate(lines):
    for col in range(num_cols):
        test_char = row[col]
        if test_char.isalnum():
            antenna_locs.append([col, line_index, test_char])


print(lines)
print()
# print(antenna_locs)

final_answer = 0

def test_letter(x, y):
    if y >= 0 and y < num_rows and x >= 0 and x < num_cols:
        return True
    return False

# def test_letter(x, y):
#     # all lines are same length
#     dirs = []
#     if y >= 0 and y < num_rows:
#         # can look N
#         dirs.append([0, -1])
#         if x >= 3:
#             # can look NW
#             dirs.append([-1, -1])
#         if dist - 1 - x >= 3:
#             # can look NE
#             dirs.append([1, -1])
    
#     if dist - 1 - x >= 3:
#         # can look E
#         dirs.append([1, 0])
#     if x >= 3:
#         # can look W
#         dirs.append([-1, 0])

#     if dist - 1 - y >= 3:
#         # can look S
#         dirs.append([0, 1])
#         if x >= 3:
#             # can look SW
#             dirs.append([-1, 1])
#         if dist - 1 - x >= 3:
#             # can look SE
#             dirs.append([1, 1])
    
#     final_dirs = dirs.copy()

#     for dir in dirs:
#         running_x = x
#         running_y = y
#         for index in range(4):
#             running_x = x + dir[0] * index
#             running_y = y + dir[1] * index
#             if lines[running_y][running_x] != test_string[index]:
#                 final_dirs.remove(dir)
#                 break
    
#     return len(final_dirs)

num_antinodes = 0
antinodes = []
for ant_a in antenna_locs:
    for ant_b in antenna_locs:
        if ant_a == ant_b:
            continue

        if ant_a[2] == ant_b[2]:
            target_a = [ant_a[0], ant_a[1]]
            target_b = [ant_b[0], ant_b[1]]
            if target_a not in antinodes and test_letter(*target_a):
                num_antinodes += 1
                antinodes.append(target_a)

            if target_b not in antinodes and test_letter(*target_b):
                num_antinodes += 1
                antinodes.append(target_b)

            dx_a = ant_b[0] - ant_a[0]
            dy_a = ant_b[1] - ant_a[1]
            a_index = 0

            while True:
                target_a = [ant_b[0] + ant_b[0] - ant_a[0] + a_index * dx_a, ant_b[1] + ant_b[1] - ant_a[1] + a_index * dy_a]
                if test_letter(*target_a):
                    if target_a not in antinodes:
                        num_antinodes += 1
                        antinodes.append(target_a)
                    a_index += 1
                else:
                    break

            # target_a = [ant_b[0] + ant_b[0] - ant_a[0], ant_b[1] + ant_b[1] - ant_a[1]]
            # target_b = [ant_a[0] - ant_b[0] - ant_a[0], ant_a[1] - ant_b[1] - ant_a[1]]
            # # abs_dist = math.sqrt((ant_b[0] - ant_a[0])**2 + (ant_b[1] - ant_a[1])**2)

            # if test_letter(*target_a):
            #     if target_a not in antinodes:
            #         num_antinodes += 1
            #         antinodes.append(target_a)
            #     # print(f"{target_a}")
            # if test_letter(*target_b):
            #     if target_b not in antinodes:
            #         num_antinodes += 1
            #         antinodes.append(target_b)
            #     # print(f"{target_b}")

antinodes.sort()
# antinodes = antinodes.sort()
print(antinodes)
print(f"num_antinodes: {num_antinodes}")
print(f"final_answer: {final_answer}") # answer: 1077