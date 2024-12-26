import math
import re
import string
lines = []
final_answer = 0
input_file_name = "test_input_1.txt" # 140
input_file_name = "test_input_2.txt" # 772
input_file_name = "test_input_3.txt" # 1930
# input_file_name = "test_input_4.txt" # 21 * 38 = 798
# # input_file_name = "test_input_5.txt"
# input_file_name = "test_input_6.txt" # 267 * 163
# input_file_name = "test_input_7.txt" # 265 * 152 = 40280 for second block
# input_file_name = "test_input_8.txt" # 68628
# input_file_name = "test_input_9.txt" # 1202
input_file_name = "test_input_10.txt" # 40 * 80 = 3200
input_file_name = "test_input_11.txt" # 50 * 96 = 4800
# input_file_name = "real_input.txt"
debug = True

def print_i(string_to_print, debug_priorty=0):
    global debug
    if debug and debug_priorty > 0:
        print(string_to_print)

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
    num_cols = len(plants[0])
    plants.insert(0, list("0" * (num_cols)))
    plants.append(list("0" * (num_cols)))
    num_rows = len(plants)

print(num_rows)
print(num_cols)

for line in plants:
    print(line)


    

def search_group(start_pos, search_char):
    global num_rows
    global num_cols
    # print(num_cols)

    if plants[start_pos[0]][start_pos[1]] != search_char:
        return 0
    
    walls = 0
    num_plants = 0

    final_score = 0
    found_plants = []
    found_plants_down = []
    found_walls = [] # should come up with a better solution than this, perhaps skipping a wall only if it has been seen in this row check already although that could get messy if plants are sepperated by a gap of one
    found_walls_down = []

    start_row = start_pos[0]
    end_row = num_rows
    
    row_starts = [start_pos[1]]
    next_row_starts = []
    next_row_tests = []

    start_col = start_pos[1]
    end_col = 0

    should_break = False
    next_row_start_index = 0
    found_edge_case = True

    locations_to_check = []
    location_to_check = []
    
    # while True:
    while True:
        # found_edge_case = False
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
                    for hor_dir in [-1, 1]: # scans columns left than right
                        for col in range(start_col+int((hor_dir+1)/2), end_col, hor_dir):
                            test_char = plants[row][col]
                            print_i(f"\ttesting x: {col}, y: {row}, hor_dir: {hor_dir}")
                            if test_char == search_char:
                                if col != start_col:
                                    if col in row_starts:
                                        col_in_row_starts = row_starts.index(col)
                                        print_i(f"\t\t\t\t[{next_row_start_index-1}] row_starts was: {row_starts}")
                                        # row_starts.pop(col_in_row_starts)
                                        row_starts[col_in_row_starts] = -1
                                        # if col_in_row_starts < col:
                                            # next_row_start_index -= 1
                                            # next_row_start_index_inc -= 1
                                        print_i(f"\t\t\t\t[{next_row_start_index-1}] row_starts is: {row_starts}")
                                if [row-vert_dir*0.1, col] not in found_plants and [row+vert_dir*0.1, col] not in found_plants:
                                # if [row-vert_dir*0.1, col] not in found_plants:
                                    num_plants += 1
                                    found_plants.append([row+vert_dir*0.1, col])
                                    # print_i(f"\t\tfound {test_char} at x: {col}, y: {row}")
                                
                                if plants[row][col+hor_dir] != search_char:
                                    if [row, col+(hor_dir * 0.25)] not in found_walls:
                                        found_walls.append([row, col+(hor_dir * 0.25)])
                                        print_i(f"\t\t\tside wall A at x: {col+hor_dir}, y: {row}, hor_dir: {hor_dir}")
                                        walls += 1
                                        should_break = True

                                if plants[row][col-hor_dir] != search_char:
                                    if [row, col-(hor_dir * 0.25)] not in found_walls:
                                        found_walls.append([row, col-(hor_dir * 0.25)])
                                        print_i(f"\t\t\tside wall A at x: {col-hor_dir}, y: {row}, hor_dir: {hor_dir} (looking back)")
                                        walls += 1
                                        # should_break = True

                                if plants[row+vert_dir][col] == test_char:
                                    # if col not in next_row_starts: # can be removed if the right pass starts at start + 1 instead of start column
                                    if col - hor_dir not in next_row_tests:
                                        next_row_starts.append(col)                                        
                                        print_i(f"\t\tnext_row_starts added x: {col}, y:{row+vert_dir}")
                                    next_row_tests.append(col)

                                elif [row+vert_dir*0.25, col] not in found_walls:
                                    print_i(f"\t\t\tvert wall at x: {col}, y: {row+vert_dir*0.25}")
                                    found_walls.append([row+vert_dir*0.25, col])
                                    walls += 1

                                # edge case where the chars zig zag horizontally
                                if plants[row-vert_dir][col] == test_char:
                                    if [row-vert_dir+vert_dir*0.1, col] not in found_plants and [row-vert_dir-vert_dir*0.1, col] not in found_plants:
                                        print_i(f"\t\t\tedge case found at x: {col}, y: {row-vert_dir}")
                                        found_edge_case = True
                                        locations_to_check.append([row-vert_dir, col])
                                
                                if should_break:
                                    should_break = False
                                    next_row_tests = []
                                    break

                            # elif [row, col] not in found_plants:
                            else:
                                # You reached the end of this wall 
                                if col == start_col + 1:
                                    if [row, col-(hor_dir * 0.75)] not in found_walls:
                                        found_walls.append([row, col-(hor_dir * 0.75)])
                                        print_i(f"\t\t\tside wall B at x: {col}, y: {row}, hor_dir: {hor_dir}")
                                        walls += 1
                                break
                            next_row_tests = []
                        end_col = num_cols
                
                if len(next_row_starts) == 0:
                    break
                
                row_starts = next_row_starts.copy()
                next_row_starts = []
        
            # found_walls = found_walls_down
            # found_plants = found_plants_down
            start_row = row
            end_row = start_pos[0]-1
        if len(locations_to_check) == 0:
            break
        else:
            # break
            location_to_check = locations_to_check.pop()
            start_pos = location_to_check
            start_row = start_pos[0]
            end_row = num_rows
            
            row_starts = [start_pos[1]]
            next_row_starts = []
            next_row_tests = []

            start_col = start_pos[1]
            end_col = 0

            should_break = False
            next_row_start_index = 0
            vert_dir = -1
    
    for plant in found_plants:
        plants[round(plant[0])][round(plant[1])] = "0"
    
    final_score += walls * num_plants
    print_i(f"num_plants: {num_plants} should equal found_plants: {found_plants}")
    assert(num_plants == len(found_plants))
    found_plants.sort()

    print_i(f"{search_char} has {num_plants} plants and {walls} walls = {final_score}", 1)
    print_i(f"plant_poses: {found_plants}")
    print_i(f"WALL_POSES: {found_walls}", 1)
    return [final_score, num_plants]



checked = []
groups = []
group_index = 0
final_answer = 0
final_num_plants = 0

for row in range(1, num_rows-1):
    for col in range(1, num_cols-1):
        # test_pos = [col, row]
        test_char = plants[row][col]
        if test_char != "0":
            print_i(f"\nstarted {test_char} at x: {col}, y: {row}")
            result = search_group([row, col], test_char)
            print_i("\n")
            final_answer += result[0]
            final_num_plants += result[1]
        # break



print("\n\n\n")

for line in plants:
    print(line)

print(f"final_num_plants: {final_num_plants}") # answer: 
print(final_answer) # answer: 
# 1420139 is too low
# 1426422 is too low
# final answer: 1433460