# Python program for A* Search Algorithm
import math
import heapq

import math
import random
import re
import string

final_answer = 0
input_file_name = "test_input_1.txt" # 140
# input_file_name = "test_input_2.txt" # 772
# input_file_name = "test_input_3.txt" # 1930
# input_file_name = "test_input_4.txt" # 21 * 38 = 798
# input_file_name = "real_input.txt"
debug = True

num_rows = 0
num_cols = 0
lines = []
direction_string = ""

def print_i(string_to_print, debug_priorty=0):
    global debug
    if debug and debug_priorty > 0:
        print(string_to_print)

class DotDict(dict):
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError as k:
            raise AttributeError(k)

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError as k:
            raise AttributeError(k)
        


# Define the Cell class
class Cell:
    def __init__(self):
      # Parent cell's row index
        self.parent_i = 0
    # Parent cell's column index
        self.parent_j = 0
 # Total cost of the cell (g + h)
        self.f = float('inf')
    # Cost from start to this cell
        self.g = float('inf')
    # Heuristic cost from this cell to destination
        self.h = 0

        self.dir = 0


# Define the size of the grid
ROW = 9
COL = 10

# Check if a cell is valid (within the grid)


def is_valid(row, col):
    return (row >= 0) and (row < ROW) and (col >= 0) and (col < COL)

# Check if a cell is unblocked


def is_unblocked(grid, row, col):
    return grid[row][col] == 1

# Check if a cell is the destination


def is_destination(row, col, dest):
    return row == dest[0] and col == dest[1]

# Calculate the heuristic value of a cell (Euclidean distance to destination)


def calculate_h_value(row, col, dest):
    return ((row - dest[0]) ** 2 + (col - dest[1]) ** 2) ** 0.5

# Trace the path from source to destination


def trace_path(cell_details, dest):
    num_turns = 0
    print("The Path is ")
    path = []
    row = dest[0]
    col = dest[1]
    dir = 0
    last_dir = 0

    # Trace the path from destination to source using parent cells
    while not (cell_details[row][col].parent_i == row and cell_details[row][col].parent_j == col):
        # path.append((row, col))
        last_dir = dir
        path.append((col, row, f"dir: {dir}"))
        temp_row = cell_details[row][col].parent_i
        temp_col = cell_details[row][col].parent_j
        row = temp_row
        col = temp_col
        dir = cell_details[row][col].dir
        if last_dir == 3 and dir == 0:
            num_turns += 1
        elif last_dir == 0 and dir == 3:
            num_turns += 1
        else:
            num_turns += abs(dir - last_dir)

    # Add the source cell to the path
    # path.append((row, col))
    path.append((col, row, f"dir: {dir}"))
    if last_dir == 3 and dir == 0:
            num_turns += 1
    elif last_dir == 0 and dir == 3:
        num_turns += 1
    else:
        num_turns += abs(dir - last_dir)
    # Reverse the path to get the path from source to destination
    path.reverse()

    # Print the path
    for i in path:
        print("->", i, end=" ")
    print(f"\npath length = {len(path)}")
    print(f"num_turns = {num_turns}")
    print(f"final_score = {len(path) + num_turns * 1000}")
    print()

# Implement the A* search algorithm


def a_star_search(grid, src, dest):
    # Check if the source and destination are valid
    if not is_valid(src[0], src[1]) or not is_valid(dest[0], dest[1]):
        print("Source or destination is invalid")
        return

    # Check if the source and destination are unblocked
    if not is_unblocked(grid, src[0], src[1]) or not is_unblocked(grid, dest[0], dest[1]):
        print("Source or the destination is blocked")
        return

    # Check if we are already at the destination
    if is_destination(src[0], src[1], dest):
        print("We are already at the destination")
        return

    # Initialize the closed list (visited cells)
    closed_list = [[False for _ in range(COL)] for _ in range(ROW)]
    # Initialize the details of each cell
    cell_details = [[Cell() for _ in range(COL)] for _ in range(ROW)]

    # Initialize the start cell details
    i = src[0]
    j = src[1]
    cell_details[i][j].f = 0
    cell_details[i][j].g = 0
    cell_details[i][j].h = 0
    cell_details[i][j].parent_i = i
    cell_details[i][j].parent_j = j

    # Initialize the open list (cells to be visited) with the start cell
    open_list = []
    heapq.heappush(open_list, (0.0, i, j))

    # Initialize the flag for whether destination is found
    found_dest = False

    # Main loop of A* search algorithm
    while len(open_list) > 0:
        # Pop the cell with the smallest f value from the open list
        p = heapq.heappop(open_list)

        # Mark the cell as visited
        i = p[1]
        j = p[2]
        closed_list[i][j] = True

        # For each direction, check the successors
        # directions = [(0, 1), (0, -1), (1, 0), (-1, 0),
        #               (1, 1), (1, -1), (-1, 1), (-1, -1)]
        # directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for dir in directions:
            new_i = i + dir[0]
            new_j = j + dir[1]

            # If the successor is valid, unblocked, and not visited
            if is_valid(new_i, new_j) and is_unblocked(grid, new_i, new_j) and not closed_list[new_i][new_j]:
                # If the successor is the destination
                if is_destination(new_i, new_j, dest):
                    # Set the parent of the destination cell
                    cell_details[new_i][new_j].parent_i = i
                    cell_details[new_i][new_j].parent_j = j
                    cell_details[new_i][new_j].dir = directions.index(dir)
                    print("The destination cell is found")
                    # Trace and print the path from source to destination
                    trace_path(cell_details, dest)
                    found_dest = True

                    return
                else:
                    # Calculate the new f, g, and h values
                    g_new = cell_details[i][j].g + 1.0
                    h_new = calculate_h_value(new_i, new_j, dest)
                    f_new = g_new + h_new

                    # If the cell is not in the open list or the new f value is smaller
                    if cell_details[new_i][new_j].f == float('inf') or cell_details[new_i][new_j].f > f_new:
                        # Add the cell to the open list
                        heapq.heappush(open_list, (f_new, new_i, new_j))
                        # Update the cell details
                        cell_details[new_i][new_j].f = f_new
                        cell_details[new_i][new_j].g = g_new
                        cell_details[new_i][new_j].h = h_new
                        cell_details[new_i][new_j].parent_i = i
                        cell_details[new_i][new_j].parent_j = j
                        cell_details[new_i][new_j].dir = directions.index(dir)

    # If the destination is not found after visiting all cells
    if not found_dest:
        print("Failed to find the destination cell")

# Driver Code


def main():

    global ROW
    global COL

    src = [-1, -1]
    dest = [-1, -1]
    grid = []
    with open(input_file_name) as file:
        # data = file.read()
        # print(data)
        # pattern = r"(?P<boxes>^#.+#$)|(?P<directions>[<^>v]+)"

        # matches = re.finditer(pattern, data, re.MULTILINE)

        x = 0
        y = 0
        for l in file:
            match = l.strip()
            x = 0
            # if match.groupdict()["boxes"]:
                # matched_string = match.groupdict()["boxes"]
                # print(f"matched boxes!: {match.groupdict()["boxes"]}")
            line = []
            for char in match:
                match char:
                    case "#":
                        line.append(0)
                    case ".":
                        line.append(1)
                    case "S":
                        # line.append("S")
                        line.append(1)
                        src = [y, x]
                    case "E":
                        # line.append("E")
                        line.append(1)
                        dest = [y, x]
                x += 1
            grid.append(line)
            y += 1

    print(f"grid: \n")
    for g in grid:
        print(g)
    
    COL = len(grid[0])
    ROW = len(grid)

    print(f"src: {src}")
    print(f"dest: {dest}")


    # Define the grid (1 for unblocked, 0 for blocked)
    # grid = [
    #     [1, 0, 1, 1, 1, 1, 0, 1, 1, 1],
    #     [1, 1, 1, 0, 1, 1, 1, 0, 1, 1],
    #     [1, 1, 1, 0, 1, 1, 0, 1, 0, 1],
    #     [0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
    #     [1, 1, 1, 0, 1, 1, 1, 0, 1, 0],
    #     [1, 0, 1, 1, 1, 1, 0, 1, 0, 0],
    #     [1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    #     [1, 0, 1, 1, 1, 1, 0, 1, 1, 1],
    #     [1, 1, 1, 0, 0, 0, 1, 0, 0, 1]
    # ]

    # Define the source and destination
    # src = [8, 0]
    # dest = [0, 0]

    # Run the A* search algorithm
    a_star_search(grid, src, dest)


if __name__ == "__main__":
    main()