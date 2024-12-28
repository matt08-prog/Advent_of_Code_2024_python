import re
import string
lines = []
final_answer = 0
input_file_name = "test_input_1.txt" # 140
# input_file_name = "test_input_2.txt" # 772
# input_file_name = "test_input_3.txt" # 1930
# input_file_name = "test_input_4.txt"
# input_file_name = "test_input_5.txt"
input_file_name = "real_input.txt"
debug = False

def test_letter(x, y):
    if y >= 0 and y < num_rows and x >= 0 and x < num_cols:
        return True
    return False

plants = []
letters = list(string.ascii_uppercase)

num_rows = 0
num_cols = 0
with open(input_file_name) as file:
    col_index = 0
    for line in file:
        stripped_line = list(line.strip())
        plants.append(["0", *stripped_line, "0"])
    num_rows = len(plants) + 1
    num_cols = len(plants[0])
    plants.insert(0, list("0" * (num_cols)))
    plants.append(list("0" * (num_cols)))

        # stones = re.findall(r"", stripped_line)

for line in plants:
    print(line)


# dirs = [[1, 0], [0, 1], [-1, 0], [0, -1]]
l_r_dirs = [[-1, 0], [1, 0]]
u_d_dirs = [[0, -1], [0, 1]]


def print_i(string_to_print):
    global debug
    if debug:
        print(string_to_print)

def search_group(start_pos, search_char):
    global num_rows
    global num_cols

    if plants[start_pos[0]][start_pos[1]] != search_char:
        return 0
    
    current_row = 0
    walls = 0
    last_char = search_char
    num_plants = 0

    final_score = 0
    found_plants = []
    found_plants_down = []
    found_walls = [] # should come up with a better solution than this, perhaps skipping a wall only if it has been seen in this row check already although that could get messy if plants are sepperated by a gap of one
    found_walls_down = []

    start_row = start_pos[0]
    end_row = num_rows
    row_inc = 1
    
    row_starts = [start_pos[1]]
    next_row_starts = []
    next_row_tests = []



    start_col = start_pos[1]
    end_col = 0
    col_inc = -1

    # for col in range(start_col, end_col, col_inc):
    #     if plants[start_row][col] == search_char and col not in next_row_starts and col + col_inc not in next_row_starts:
    #         next_row_starts.append([start_row, col])
    
    # for col in range(start_col+1, num_cols, 1):
    #     if plants[start_row][col] == search_char and col not in next_row_starts and col + col_inc not in next_row_starts:
    #         next_row_starts.append([start_row, col])

    next_row_start_index = 0
    for vert_dir in [1, -1]: # scans rows top to bottom then bottom to top
        for row in range(start_row, end_row, vert_dir):
            print_i(f"****searching row {row} in direction {vert_dir}****")
            next_row_start_index = 0
            print_i(f"************row_starts: {row_starts}")
            while next_row_start_index < len(row_starts) and next_row_start_index >= 0: # >= 0 check is redundant
                start_col = row_starts[next_row_start_index]
                if start_col == -1:
                    next_row_start_index += 1
                    continue
                next_row_start_index += 1

                print_i(f"*****starting fom column: {start_col}")
                end_col = 0
                next_row_start_index_inc = 1
                for hor_dir in [-1, 1]: # scans columns left than right
                    for col in range(start_col+int((hor_dir+1)/2), end_col, hor_dir):
                        test_char = plants[row][col]
                        print_i(f"\ttesting x: {col}, y: {row}, hor_dir: {hor_dir}")
                        if test_char == search_char:
                            if col != start_col: # redundant
                                if col in row_starts:
                                    col_in_row_starts = row_starts.index(col)
                                    print_i(f"\t\t\t\t[{next_row_start_index-1}] row_starts was: {row_starts}")
                                    # row_starts.pop(col_in_row_starts)
                                    row_starts[col_in_row_starts] = -1
                                    # if col_in_row_starts < col:
                                        # next_row_start_index -= 1
                                        # next_row_start_index_inc -= 1
                                    print_i(f"\t\t\t\t[{next_row_start_index-1}] row_starts is: {row_starts}")
                            if [row, col] not in found_plants:
                                num_plants += 1
                                found_plants_down.append([row, col])
                                # print_i(f"\t\tfound {test_char} at x: {col}, y: {row}")
                                
                                if plants[row][col+hor_dir] != search_char:
                                    if [row, col+(hor_dir * 0.25)] not in found_walls:
                                        found_walls_down.append([row, col+(hor_dir * 0.25)])
                                        print_i(f"\t\t\tside wall A at x: {col+hor_dir}, y: {row}, hor_dir: {hor_dir}")
                                        walls += 1

                            if plants[row+vert_dir][col] == test_char:
                                if col not in next_row_starts: # can be removed if the right pass starts at start + 1 instead of start column
                                    if col - hor_dir not in next_row_tests:
                                        next_row_starts.append(col)
                                        # check if first element in searched row has left wall or if last element in searched row has right wall
                                        
                                        # print_i(f"\t\tnext_row_starts added x: {col}, y:{row+vert_dir}")
                                    next_row_tests.append(col)

                            else:
                                # if [row+vert_dir, col] not in found_walls_down: Redundant?
                                # print_i(f"\t\t\tvert wall at x: {col}, y: {row+vert_dir}")
                                # found_walls.append([row+vert_dir, col])
                                walls += 1

                        elif [row, col] not in found_plants:
                            # You reached the end of this wall 
                            if col == start_col + 1:
                                if [row, col-(hor_dir * 0.75)] not in found_walls:
                                    found_walls_down.append([row, col-(hor_dir * 0.75)])
                                    print_i(f"\t\t\tside wall B at x: {col}, y: {row}, hor_dir: {hor_dir}")
                                    walls += 1
                            # if hor_dir == 1:
                            #     next_row_start_index += 1
                            # if next_row_start_index_inc == 0:
                            #     next_row_start_index += 1
                            #     next_row_start_index_inc = 0
                            
                            break
                        # current_row += 1
                        next_row_tests = []
                    end_col = num_cols
            
            if len(next_row_starts) == 0:
                break
            
            row_starts = next_row_starts.copy()
            next_row_starts = []

        
        found_walls = found_walls_down
        found_plants = found_plants_down
        start_row = row
        end_row = start_pos[0]-1
        # current_row = 0
    
    for plant in found_plants:
        plants[plant[0]][plant[1]] = "0"
    
    final_score += walls * num_plants

    found_plants.sort()

    print_i(f"{search_char} has {num_plants} plants and {walls} walls = {final_score}")
    print_i(f"plant_poses: {found_plants}")
    return final_score



checked = []
groups = []
group_index = 0
final_answer = 0

for row in range(num_rows):
    for col in range(num_cols):
        # test_pos = [col, row]
        test_char = plants[row][col]
        if test_char != "0":
            print_i(f"\nstarted {test_char} at x: {col}, y: {row}")
            result = search_group([row, col], test_char)
            print_i("\n")
            final_answer += result


        # for dir in dirs:

print("\n\n\n")

for line in plants:
    print(line)

print(final_answer) # answer: 
# 1420139 is too low