# Python program for A* Search Algorithm
import math
import heapq

import math
import random
import re
import string

# # Set up the display
# scale = 2.0
# WIDTH, HEIGHT = int(400*scale), int(300*scale)
# GRID_SIZE = int(20*scale)
# SCREEN = None

import pygame
import sys

# Set up the display
WIDTH, HEIGHT = 1080, 720
SCREEN = None

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (50, 50, 50)

class Camera:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.x = 0
        self.y = 0
        self.zoom = 1

    def apply(self, x, y):
        return ((x - self.x) * self.zoom, (y - self.y) * self.zoom)

    def reverse_apply(self, x, y):
        return (x / self.zoom + self.x, y / self.zoom + self.y)

camera = Camera(WIDTH, HEIGHT)

def draw_grid(start, end, walls, paths, final_path):
    global SCREEN
    SCREEN.fill(WHITE)
    
    # grid_size = int(20 * camera.zoom)
    grid_size = 20 * camera.zoom
    # grid_size = int(camera.apply(20 * camera.zoom, 20 * camera.zoom)[0])
    
    # # Draw grid lines
    # for x in range(0, WIDTH, grid_size):
    #     start_pos = camera.apply(x, 0)
    #     end_pos = camera.apply(x, HEIGHT)
    #     pygame.draw.line(SCREEN, BLACK, start_pos, end_pos)
    # for y in range(0, HEIGHT, grid_size):
    #     start_pos = camera.apply(0, y)
    #     end_pos = camera.apply(WIDTH, y)
    #     pygame.draw.line(SCREEN, BLACK, start_pos, end_pos)
    
    # Draw squares at specified positions
    for pos in [start, end]:
        x, y = camera.apply(pos[0] * grid_size, pos[1] * grid_size)
        # gs = camera.apply(grid_size, grid_size)[0]
        gs = grid_size * camera.zoom
        pygame.draw.rect(SCREEN, RED, (x, y, gs, gs))

    # Draw walls
    for pos in walls:
        x, y = camera.apply(pos[0] * grid_size, pos[1] * grid_size)
        # pygame.draw.rect(SCREEN, BLACK, (x, y, grid_size, grid_size))

        # gs = camera.apply(grid_size, grid_size)[0]
        # gs = camera.apply(grid_size * camera.zoom, grid_size * camera.zoom)[0]
        gs = grid_size * camera.zoom
        pygame.draw.rect(SCREEN, BLACK, (x, y, gs, gs))

    # Draw path squares and render score text
    # font = pygame.font.Font(None, int(grid_size * 0.3))
    font = pygame.font.Font(None, int(grid_size * camera.zoom * 0.3))
    for pos in paths:
        x, y, score = pos
        x, y = camera.apply(x * grid_size, y * grid_size)
        # pygame.draw.rect(SCREEN, GRAY, (x, y, grid_size, grid_size))
        # gs = camera.apply(grid_size, grid_size)[0]
        gs = grid_size * camera.zoom
        pygame.draw.rect(SCREEN, GRAY, (x, y, gs, gs))

        # Render score text
        text = font.render(str(score), True, WHITE)
        text_rect = text.get_rect(center=(x + grid_size // 2, y + grid_size // 2))
        SCREEN.blit(text, text_rect)
    
    for pos in final_path:
        x, y, score = pos
        x, y = camera.apply(x * grid_size, y * grid_size)
        # pygame.draw.rect(SCREEN, GREEN, (x, y, grid_size, grid_size))
        # gs = camera.apply(grid_size, grid_size)[0]
        gs = grid_size * camera.zoom
        pygame.draw.rect(SCREEN, GREEN, (x, y, gs, gs))


        # Render score text
        text = font.render(str(score), True, BLACK)
        text_rect = text.get_rect(center=(x + grid_size // 2, y + grid_size // 2))
        SCREEN.blit(text, text_rect)

    pygame.display.flip()

def main_pygame(start, end, walls, paths, final_path):
    global SCREEN
    
    # Initialize Pygame
    pygame.init()
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Grid with Squares, Walls, and Scores")

    running = True
    panning = False
    pan_start = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    panning = True
                    pan_start = event.pos
                elif event.button == 4:  # Mouse wheel up
                    camera.zoom *= 1.1
                    # camera.x += event.pos[0] / camera.zoom
                    # camera.x += (event.pos[0] * 1.2) 
                    # camera.x *= (event.pos[0] / WIDTH) * 1.1
                    # camera.x += event.pos[0]
                elif event.button == 5:  # Mouse wheel down
                    camera.zoom /= 1.1
                    # camera.x -= event.pos[0] / camera.zoom
                    # camera.x -= (event.pos[0] * 2.2) 
                    # camera.x *= -(event.pos[0] / WIDTH) * 1.1
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left mouse button
                    panning = False
            elif event.type == pygame.MOUSEMOTION:
                if panning:
                    dx, dy = event.pos[0] - pan_start[0], event.pos[1] - pan_start[1]
                    camera.x -= dx / camera.zoom
                    camera.y -= dy / camera.zoom
                    pan_start = event.pos
        
        draw_grid(start, end, walls, paths, final_path)
    
    pygame.quit()

def get_color(seed):
    random.seed(seed)
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

final_answer = 0
input_file_name = "test_input_1.txt" # 7036
input_file_name = "test_input_2.txt" # 11048
# input_file_name = "test_input_3.txt" # 1930
# input_file_name = "test_input_4.txt" # 21 * 38 = 798
input_file_name = "real_input.txt"
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
        # self.f = float('inf')
        self.fs = {}
    # Cost from start to this cell
        self.g = float('inf')
    # Heuristic cost from this cell to destination
        self.h = 0

        self.dir = -1

        self.parent_dir = -1
        self.num_turns_from = {}


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

def calc_dir_dist(dir_1, dir_2):
    dir_dist = abs((dir_1 + int(dir_1 == 0 and dir_2 == 3) * 4) - (dir_2 + int(dir_2 == 0 and dir_1 == 3) * 4))
    
    return dir_dist

def trace_path(cell_details, src, dest):
    # to make up for when we check the destination whose final direction doesn't matter
    num_turns = 0
    print("The Path is ")
    path = []
    row = dest[0]
    col = dest[1]
    dir = cell_details[row][col].dir
    last_dir = cell_details[row][col].dir

    # for cd_y in range(len(cell_details)):
    #     for cd_x in range(len(cell_details[0])):
    #         cd = cell_details[cd_y][cd_x]
    #         print_i(f"\tCD[{[cd_x, cd_y]}]: g = {cd.g}, dir = {cd.dir}, parent = {[cd.parent_j, cd.parent_i]}")
    
    possibilities = []

    # works becaue the parent of src is src
    # Trace the path from destination to source using parent cells
    temp_g = 0
    while not (cell_details[row][col].parent_i == row and cell_details[row][col].parent_j == col):
        # path.append((row, col))
        possibilities.append([row, col])
        last_dir = dir
        # path.append((col, row, f"dir: {dir}"))
        # path.append([col, row])
        temp_row = cell_details[row][col].parent_i
        temp_col = cell_details[row][col].parent_j
        temp_g = cell_details[row][col].g
        path.append((col, row, temp_g))
        row = temp_row
        col = temp_col
        dir = cell_details[row][col].dir
        # if last_dir == 3 and dir == 0:
        #     num_turns += 1
        # elif last_dir == 0 and dir == 3:
        #     num_turns += 1
        # else:
        #     num_turns += abs(dir - last_dir)
        num_turns += calc_dir_dist(dir, last_dir)

    # Add the source cell to the path
    # path.append((row, col))
    # path.append((col, row, f"dir: {dir}"))
    # path.append([col, row])
    # path.append((col, row))
    temp_g = cell_details[row][col].g
    path.append((col, row, temp_g))
    # num_turns += calc_dir_dist(dir, last_dir)
    # Reverse the path to get the path from source to destination
    path.reverse()



    walls = []
    opens = []
    for cd_y in range(len(cell_details)):
        for cd_x in range(len(cell_details[0])):
            cd = cell_details[cd_y][cd_x]
            print_i(f"\tCD[{[cd_x, cd_y]}]: g = {cd.g}, dir = {cd.dir}, parent = {[cd.parent_j, cd.parent_i]}")
            if cd.dir == -1:
                walls.append([cd_x, cd_y])
            elif [cd_x, cd_y] != src and [cd_x, cd_y] != dest:
                opens.append([cd_x, cd_y, cd.g])
            # elif [x, y] in path:
            #     opens.remove()
    main_pygame(src, dest, walls, opens, path)



    # Print the path
    for i in path:
        print("->", i, end=" ")
    print(f"\npath length = {len(path) - 1}")
    print(f"num_turns = {num_turns}")
    print(f"final_score = {len(path) - 1 + num_turns * 1000}")
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

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    # Initialize the closed list (visited cells)
    closed_list = [[False for _ in range(COL)] for _ in range(ROW)]
    # Initialize the details of each cell
    cell_details = [[Cell() for _ in range(COL)] for _ in range(ROW)]

    # for cd_y in range(len(cell_details)):
    #     for cd_x in range(len(cell_details[0])):
    #         for dir in directions:
    #             num_turns_from.append

    # Initialize the start cell details
    i = src[0]
    j = src[1]
    cell_details[i][j].f = 0
    cell_details[i][j].g = 0
    cell_details[i][j].h = 0
    cell_details[i][j].parent_i = i
    cell_details[i][j].parent_j = j
    cell_details[i][j].dir = 0

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
        


        for dir in directions:
            new_i = i + dir[0]
            new_j = j + dir[1]

            # If the successor is valid, unblocked, and not visited
            if is_valid(new_i, new_j) and is_unblocked(grid, new_i, new_j) and not closed_list[new_i][new_j]:
                print_i(f"testing [{[j, i]}], dir: {cell_details[i][j].dir}")
                # If the successor is the destination
                if is_destination(new_i, new_j, dest):
                    # Set the parent of the destination cell
                    cell_details[new_i][new_j].parent_i = i
                    cell_details[new_i][new_j].parent_j = j

                    p_i = i
                    p_j = j
                    cell_details[new_i][new_j].parent_dir = cell_details[p_i][p_j].dir
                    cell_details[new_i][new_j].dir = directions.index(dir)
                    print("\n\n\n\nThe destination cell is found")
                    
                    # Trace and print the path from source to destination
                    trace_path(cell_details, src, dest)
                    found_dest = True

                    return
                else:
                    dir_dist = calc_dir_dist(directions.index(dir), cell_details[i][j].dir)
                    print_i(f"\tcomparing last dir {cell_details[i][j].dir} to new dir {directions.index(dir)} = {dir_dist}")

                    assert(cell_details[i][j].dir != -1)
                    
                    # Calculate the new f, g, and h values
                    g_new = cell_details[i][j].g + 1.0 + dir_dist * 1000
                    print_i(f"\t\tg went from {cell_details[i][j].g} to {g_new}")

                    h_new = calculate_h_value(new_i, new_j, dest)
                    # h_new = 0
                    # f_new = g_new + h_new
                    f_new = g_new + h_new
                    old_coords = str([i, j])

                    should_update_cell = False
                    # If the cell is not in the open list or the new f value is smaller
                    # if cell_details[new_i][new_j].f == float('inf') or cell_details[new_i][new_j].f > f_new:
                    if old_coords not in cell_details[new_i][new_j].fs.keys():
                        should_update_cell = True
                    
                    elif cell_details[new_i][new_j].fs[old_coords] > f_new:
                        should_update_cell = True
                        
                    if should_update_cell:
                        should_update_cell = False
                        # Add the cell to the open list
                        heapq.heappush(open_list, (f_new, new_i, new_j))
                        # Update the cell details
                        # cell_details[new_i][new_j].f = f_new
                        cell_details[new_i][new_j].fs[old_coords] = f_new
                        cell_details[new_i][new_j].g = g_new
                        cell_details[new_i][new_j].h = h_new
                        cell_details[new_i][new_j].parent_i = i
                        cell_details[new_i][new_j].parent_j = j

                        p_i = i
                        p_j = j
                        cell_details[new_i][new_j].parent_dir = cell_details[p_i][p_j].dir
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

    print(f"src: {[src[1], src[0]]}")
    print(f"dest: {[dest[1], dest[0]]}")


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
    # a_star_search(grid, dest, src)


if __name__ == "__main__":
    main()

# 94448 is too high