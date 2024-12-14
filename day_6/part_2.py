import re
# input_file_name = "test_input_1.txt"
# input_file_name = "test_input_2.txt"
# input_file_name = "test_input_4.txt"
# input_file_name = "test_input_5.txt"
# input_file_name = "test_input_6.txt"
input_file_name = "test_input_7.txt"
# input_file_name = "real_input.txt"
lines = []
walls = []
char_index = 0
start_pos = 0
num_unique_positions = 1
max_turns_taken = 10000
debug = True


def replace_char(col, row, new_char):
    global num_unique_positions

    line_to_replace = lines[row]
    old_char = line_to_replace[col]
    # if old_char == "#":
    #     return True
    # elif old_char == ".":
    #     num_unique_positions += 1
    
    lines[row] = line_to_replace[:col] + new_char + line_to_replace[col+1:]
    
    return old_char

first_pass = True

def test_and_replace_char(col, row, new_char):
    global num_unique_positions
    global poses_to_test
    global first_pass

    line_to_replace = lines[row]
    old_char = line_to_replace[col]
    if old_char == "#" or old_char == "O":
        return True
    elif old_char == "." and first_pass:
        num_unique_positions += 1
    elif first_pass and ((old_char == "|" and new_char == "-")or (old_char == "-" and new_char == "|")):
        new_char = "+"
    elif first_pass and old_char == "+":
        new_char = "+"
    old_num = len(lines[row])
    assert(len(lines[row]) == num_columns)
    assert(len(new_char) == 1)
    assert(len(line_to_replace) == num_columns)
    # assert(len(line_to_replace[:col]) == col)
    if first_pass:
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
last_dir = -1
num_rows = len(lines)
num_columns = len(lines[0])
num_spots = num_rows * num_columns

curr_row = int(start_pos / num_columns)
curr_column = start_pos % num_columns
test_and_replace_char(curr_column, curr_row, "S")
new_char_lr = "-"
new_char_ud = "|"


num_places = 0
for l in lines:
    for c in l:
        num_places += 1
print(f"num_places {num_places} == {num_spots}")

poses_to_test = []
tested_poses = []


def should_place(added_row, added_column, dir):
    global first_pass

    # if not first_pass:
    #     print("added pose")
    #     pass
    # else:
    if first_pass and [added_row, added_column, dir] not in poses_to_test:
        poses_to_test.append([added_row, added_column, dir])
    
    return False

num_loops = 0
loops = []

def test_loop(added_row, added_column):
    global dir
    global last_dir
    global curr_row
    global curr_column
    global num_loops
    global loops
    global max_turns_taken

    num_turns = 0

    if added_row != -1:
        curr_row = added_row
        curr_column = added_column
    
    initial_dir = dir - 1
    if initial_dir == -1:
        initial_dir = 3
    initial_dir = initial_dir % 4

    while True:
        # print(f"curr_row: {curr_row}")
        # print(f"curr_column: {curr_column}")
        # print(f"dir: {dir}")

        if dir == 3: # up
            for row in range(curr_row, -2, -1):
                if row >= 0:
                    if test_and_replace_char(curr_column, row, new_char_ud):
                        # dir += 1
                        break
                    should_place(row, curr_column, dir)
                curr_row = row
        elif dir == 0: # right
            for col in range(curr_column, num_columns + 1, 1):
                if col + 1 <= num_columns:
                    if test_and_replace_char(col, curr_row, new_char_lr):
                        # dir += 1
                        break
                    should_place(curr_row, col, dir)
                curr_column = col
        elif dir == 1: # down
            for row in range(curr_row, num_rows + 1, 1):
                if row + 1 <= num_rows:
                    if test_and_replace_char(curr_column, row, new_char_ud):
                        # dir += 1
                        break
                    should_place(row, curr_column, dir)
                curr_row = row
        elif dir == 2: # left
            for col in range(curr_column, -2, -1):
                if col >= 0:
                    if test_and_replace_char(col, curr_row, new_char_lr):
                        break
                    should_place(curr_row, col, dir)
                curr_column = col

        if curr_column < 0 or curr_row < 0:
            break
        if curr_column >= num_columns or curr_row >= num_rows:
            break

        if not first_pass:
            if curr_column == added_column and curr_row == added_row and num_turns > 2 and dir == initial_dir:
            # if curr_column == added_column and curr_row == added_row and num_turns > 2:
                # if num_loops > 0:
                #     exit(-1)
                # loops.append([curr_row, curr_column])
                num_loops += 1
                return True
            if num_turns > max_turns_taken:
                return

        dir += 1
        dir = dir % 4
        last_dir = dir
        num_turns += 1
    return False

test_loop(-1, -1)

first_pass = False
print(f"Finished first pass")

for line in lines:
    print(line)

print()
poses_to_test.pop(0)
print(f"poses_to_test: {poses_to_test}")
print(f"nunm_poses_to_test: {len(poses_to_test)}")

i = 1
found_match = True
while found_match == True:
    found_match = False
    i = 1
    while i < len(poses_to_test) - 1:
        # if poses_to_test[i][2] != poses_to_test[i-1][2] and poses_to_test[i][0:2] == poses_to_test[i-1][0:2]:
        if poses_to_test[i][0:2] == poses_to_test[i-1][0:2]:
            poses_to_test.pop(i)
            found_match = True

        i += 1

for coords in poses_to_test:
    # if debug:
    #     print(f"\ncoords: {coords}")
    # print(curr_column)

    dir = coords[2]
    old_row = coords[0]
    old_col = coords[1]

    if dir == 1:
        curr_row = old_row - 1
        curr_column = old_col
    if dir == 3:
        curr_row = old_row + 1
        curr_column = old_col
    
    if dir == 0:
        curr_row = old_row
        curr_column = old_col - 1
    if dir == 2:
        curr_row = old_row
        curr_column = old_col + 1
    
    # print(curr_column)
    # print(f"coords: {coords}")
    # print(f"old coord [{old_row}, {old_col}]")
    # print(f"new coords [{curr_row}, {curr_column}]")

    dir += 1
    dir = dir % 4

    old_char = replace_char(old_col, old_row, "O")

    old_char_1 = replace_char(curr_column, curr_row, str(dir))
    if debug:
        for line in lines:
            print(line)
        # print()
    replace_char(curr_column, curr_row, old_char_1)

    if test_loop(curr_row, curr_column):
        loops.append([old_row, old_col])
        if debug:
            print(f"Loop found: ({old_row}, {old_col})")
    if debug:
        print()

    old_char = replace_char(old_col, old_row, old_char)

for line in lines:
    print(line)

num_places = 0
for l in lines:
    for c in l:
        num_places += 1

def unique_list_count(list_of_lists):
    # Convert each list to a tuple to make them hashable
    tuple_list = [tuple(lst) for lst in list_of_lists]

    # Create a set to get unique tuples
    unique_tuples = set(tuple_list)

    # Return the number of unique tuples
    return len(unique_tuples)

print(f"num_places {num_places}")
print(f"num_unique_positions: {num_unique_positions}")
print(f"num_poses: {len(poses_to_test)}")
print(f"num_loops: {num_loops}")
print(f"loops: {loops}")
print(f"num_unique: {unique_list_count(loops)}")
assert(num_loops == len(loops))
# print(f"{lines[0][4]}")
exit(-1)

# answer: 556 is too low
# answer: 768 is too low

# answer: 1865 is too high
# answer: 1632 is wrong
# answer: 1742 is wrong
# answer: 1706 is wrong

