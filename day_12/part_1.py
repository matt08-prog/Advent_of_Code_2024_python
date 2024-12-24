import re
import string
lines = []
final_answer = 0
input_file_name = "test_input_1.txt"
input_file_name = "test_input_2.txt"
# input_file_name = "test_input_3.txt"
# input_file_name = "test_input_4.txt"
# input_file_name = "test_input_5.txt"
# input_file_name = "real_input.txt"

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

debug = True

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
    found_walls = [] # should come up with a better solution than this, perhaps skipping a wall only if it has been seen in this row check already although that could get messy if plants are sepperated by a gap of one

    start_row = start_pos[0]
    end_row = num_rows
    row_inc = 1
    
    row_starts = [start_pos[1]]
    next_row_starts = []

    start_col = start_pos[1]
    end_col = 0
    col_inc = -1


    # for col in range(start_col, end_col, col_inc):
    #     if plants[start_row][col] == search_char and col not in next_row_starts and col + col_inc not in next_row_starts:
    #         next_row_starts.append([start_row, col])
    
    # for col in range(start_col+1, num_cols, 1):
    #     if plants[start_row][col] == search_char and col not in next_row_starts and col + col_inc not in next_row_starts:
    #         next_row_starts.append([start_row, col])

    for vert_dir in [1, -1]: # scans rows top to bottom then bottom to top
        for row in range(start_row, end_row, vert_dir):
            print_i(f"****searching row {row} in direction {vert_dir}****")
            # start_col = start_pos[1]
            end_col = 0
            for start_col in row_starts:
                # already_found = False
                for hor_dir in [-1, 1]: # scans columns left than right
                    for col in range(start_col, end_col, hor_dir):
                        test_char = plants[row][col]
                        if test_char == search_char:
                            if [row, col] not in found_plants:
                                num_plants += 1
                                found_plants.append([row, col])
                                print_i(f"found {test_char} at x: {col}, y: {row}")
                                
                                # if col == 0 and [-1, row] not in found_walls:
                                #     print_i(f"\t\tside wall A at x: {-1}, y: {row}")
                                #     found_walls.append([-1, row])
                                #     walls += 1 # hit a wall on left or right side
                                # if col == num_cols - 1 and [num_cols, row] not in found_walls:
                                #     print_i(f"\t\tside wall B at x: {num_cols}, y: {row}")
                                #     found_walls.append([num_cols, row])
                                #     walls += 1 # hit a wall on left or right side

                                
                                if col == 1: # redundant
                                    if [row, 0] not in found_walls:
                                        print_i(f"\t\tside wall A at x: {0}, y: {row}")
                                        found_walls.append([row, 0])
                                        walls += 1 # hit a wall on left or right side
                                elif plants[row][col-hor_dir] != search_char:
                                    if [row, col-hor_dir] not in found_walls:
                                        print_i(f"\t\tside wall B at x: {col-hor_dir}, y: {row}")
                                        walls += 1
                                if col == num_cols - 2: # redundant
                                    if [row, num_cols-1] not in found_walls:
                                        print_i(f"\t\tside wall C at x: {num_cols-1}, y: {row}")
                                        found_walls.append([row, num_cols-1])
                                        walls += 1 # hit a wall on left or right side
                                elif plants[row][col+hor_dir] != search_char:
                                    if [row, col+hor_dir] not in found_walls:
                                        print_i(f"\t\tside wall D at x: {col+hor_dir}, y: {row}")
                                        walls += 1

                            if plants[row+vert_dir][col] == test_char:
                                if col not in next_row_starts:
                                    if col - hor_dir not in next_row_starts:
                                        next_row_starts.append(col)
                                        # check if first element in searched row has left wall or if last element in searched row has right wall
                                        
                                        print_i(f"\tnext_row_starts added x: {col}, y:{row+1}")
                                    

                            else:
                                if [row+vert_dir, col] not in found_walls:
                                    print_i(f"\t\tvert wall at x: {col}, y: {row+vert_dir}")
                                    found_walls.append([row+vert_dir, col])
                                    walls += 1
                            # if current_row == 0: # just makes it easier so don't have to check edge conditions on top row of input
                            #     print_i(f"\t\twall at x: {col}, y: {row-vert_dir}")
                            #     walls += 1 # hit a wall on top or bottom
                            # elif test_char != plants[row+vert_dir][col]:
                            #     print_i(f"\t\twall at x: {col}, y: {row+vert_dir}")
                            #     walls += 1 # hit a wall on top or bottom
                        elif [row, col] not in found_plants:
                            # You reached the end of this wall 
                            break
                # if col > 0:
                #     if plants[row][start_col - 1] != 
                #     print_i(f"\t\tside wall C at x: {col}, y: {row}")
                #     found_walls.append([row, col])
                #     walls += 1 # hit a wall on left or right side
                        # else:
                        #     if test_char != last_char and test_char != "0":
                        #         result = search_group([row,col], test_char)
                        #         print(f"{test_char}: {result}")
                        #         final_score += result
                        # last_char = test_char
                        current_row += 1
                    
                    # walls += 1
                # start_col = start_pos[1]
                    end_col = num_cols
            if len(next_row_starts) == 0:
                break
            row_starts = next_row_starts.copy()
            next_row_starts = []
                # col_inc = 1
            # start_pos[1] = next_row_start
            
        start_row = row
        end_row = start_pos[0]-1
        current_row = 0
    
    for plant in found_plants:
        plants[plant[0]][plant[1]] = "0"
    
    final_score += walls * num_plants

    print_i(f"{search_char} has {num_plants} plants and {walls} walls = {final_score}")

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

for line in plants:
    print(line)

print(final_answer) # answer: 185205