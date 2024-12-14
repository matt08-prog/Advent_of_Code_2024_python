import re
# input_file_name = "test_input_1.txt"
# input_file_name = "test_input_2.txt"
input_file_name = "real_input.txt"
lines = []
walls = []
char_index = 0
start_pos = 0
num_unique_positions = 1

def test_and_replace_char(col, row, new_char):
    global num_unique_positions

    line_to_replace = lines[row]
    old_char = line_to_replace[col]
    if old_char == "#":
        return True
    elif old_char == ".":
        num_unique_positions += 1
    old_num = len(lines[row])
    assert(len(lines[row]) == num_columns)
    assert(len(new_char) == 1)
    assert(len(line_to_replace) == num_columns)
    # assert(len(line_to_replace[:col]) == col)
    lines[row] = line_to_replace[:col] + new_char + line_to_replace[col+1:]
    # print(lines[row])
    # print(dir)
    # assert(len(lines[row]) == old_num)
    return False


with open(input_file_name) as file:
    input_lines = file.readlines()
    
    for line in input_lines:
        lines.append(line.strip())
        for char in line:
            if char == ".":
                char_index += 1
            elif char == "#":
                walls.append(char_index)
                char_index += 1
            elif char == "^":
                start_pos = char_index
                char_index += 1

dir = 3 # up
num_rows = len(lines)
num_columns = len(lines[0])
num_spots = num_rows * num_columns

curr_row = int(start_pos / num_columns)
curr_column = start_pos % num_columns
test_and_replace_char(curr_column, curr_row, "S")
new_char = "-"


num_places = 0
for l in lines:
    for c in l:
        num_places += 1
print(f"num_places {num_places} == {num_spots}")

while True:
    # print(f"curr_row: {curr_row}")
    # print(f"curr_column: {curr_column}")

    if dir == 3: # up
        for row in range(curr_row, -2, -1):
            if row >= 0:
                if test_and_replace_char(curr_column, row, new_char):
                    dir += 1
                    break
            curr_row = row
    elif dir == 0: # right
        for col in range(curr_column, num_columns + 1, 1):
            if col + 1 <= num_columns:
                if test_and_replace_char(col, curr_row, new_char):
                    dir += 1
                    break
            curr_column = col
    elif dir == 1: # down
        for row in range(curr_row, num_rows + 1, 1):
            if row + 1 <= num_rows:
                if test_and_replace_char(curr_column, row, new_char):
                    dir += 1
                    break
            curr_row = row
    elif dir == 2: # left
        for col in range(curr_column, -2, -1):
            if col >= 0:
                if test_and_replace_char(col, curr_row, new_char):
                    dir += 1
                    break
            curr_column = col

    if curr_column < 0 or curr_row < 0:
        break
    if curr_column >= num_columns or curr_row >= num_rows:
        break

    dir = dir % 4
    # print(f"dir: {dir}")
    # curr_row = int(start_pos / num_columns)
    # curr_column = start_pos % num_columns
    # break

for line in lines:
    print(line)

num_places = 0
for l in lines:
    for c in l:
        num_places += 1
print(f"num_places {num_places}")
# answer: 5240 is too high
print(f"final answer: {num_unique_positions}") # final answer: 5239
exit(-1)

#     if line != "\n":
#         # print(line[0:2])
#         rules.append([int(line[0:2]), int(line[3:5])])
#         start_of_updates += 1
#     else:
#         start_of_updates += 1
#         break
# for line in lines[start_of_updates:]:
#     stripped_line = line.strip().split(",")
#     int_array = [int(i) for i in stripped_line]
#     updates.append(int_array)

# print(f"lines: {lines}")

# # print(f"updates: {updates}")

# final_answer = 0

# print(f"final_answer: {final_answer}")
