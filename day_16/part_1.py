import math
import random
import re
import string

import pygame
import sys

# Set up the display
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 20
SCREEN = None

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


def draw_grid(robot_pos, walls, boxes):
    global SCREEN
    SCREEN.fill(WHITE)
    
    # Draw grid lines
    for x in range(0, WIDTH, GRID_SIZE):
        pygame.draw.line(SCREEN, BLACK, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, GRID_SIZE):
        pygame.draw.line(SCREEN, BLACK, (0, y), (WIDTH, y))
    
    # Draw squares at specified positions
    for pos in [robot_pos]:
        x, y = pos
        pygame.draw.rect(SCREEN, RED, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    # Draw squares at specified positions
    for pos in walls:
        x, y = pos
        pygame.draw.rect(SCREEN, BLACK, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    # Draw squares at specified positions
    for pos in boxes:
        x, y = pos
        pygame.draw.rect(SCREEN, GREEN, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    
    # # Draw red X's at wall positions
    # for wall in walls:
    #     y, x, color_index = wall
    #     center_x = x * GRID_SIZE + GRID_SIZE // 2
    #     center_y = y * GRID_SIZE + GRID_SIZE // 2
    #     # color = get_color(color_index)
    #     color = BLACK
    #     size = GRID_SIZE // 4
    #     pygame.draw.line(SCREEN, color, (center_x - size, center_y - size), (center_x + size, center_y + size), 2)
    #     pygame.draw.line(SCREEN, color, (center_x - size, center_y + size), (center_x + size, center_y - size), 2)

    

    pygame.display.flip()

def main(robot_pos, walls, boxes):
    global SCREEN
    # Example grid positions and walls
    # positions = [(1, 1), (3, 3), (5, 2)]
    # walls = [(2, 1), (3, 2), (4, 3)]
    
    # Initialize Pygame
    pygame.init()
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Grid with Squares and Walls")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Check if the ESC key is pressed
                    running = False
        
        draw_grid(robot_pos, walls, boxes)
    
    pygame.quit()
    # sys.exit()

def get_color(seed):
    random.seed(seed)
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

# if __name__ == "__main__":
#     main()



lines = []
final_answer = 0
input_file_name = "test_input_1.txt" # 140
input_file_name = "test_input_2.txt" # 772
# input_file_name = "test_input_3.txt" # 1930
# input_file_name = "test_input_4.txt" # 21 * 38 = 798
# # input_file_name = "test_input_5.txt"
# input_file_name = "test_input_6.txt" # 267 * 163
# input_file_name = "test_input_7.txt" # 265 * 152 = 40280 for second block
# input_file_name = "test_input_8.txt" # 68628
# input_file_name = "test_input_9.txt" # 1202
# input_file_name = "test_input_10.txt" # 40 * 80 = 3200
# input_file_name = "test_input_11.txt" # 50 * 96 = 4800
# input_file_name = "test_input_12.txt" # 50 * 96 = 4800
input_file_name = "real_input.txt"
debug = True

def print_i(string_to_print, debug_priorty=0):
    global debug
    if debug and debug_priorty > 0:
        print(string_to_print)

def test_letter(x, y):
    global num_rows
    global num_cols
    if y >= 0 and y < num_rows and x >= 0 and x < num_cols:
        return True
    return False

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

robots = []
letters = list(string.ascii_uppercase)

num_rows = 0
num_cols = 0
lines = []
direction_string = ""

with open(input_file_name) as file:
    # col_index = 0
    
    # num_cols = 11 # 101 
    num_cols = 101 
    # num_rows = 7 # 103
    num_rows = 103
    data = file.read()

    # for line in file:
    # robot = {}
    # stripped_line = line.strip()
    print(data)
    # pattern = r"\n#(.+)#$^[\^<>V]"
    # pattern = r"((\n#(.+)#$)|(?P<directions>[<^>v]+))"
    pattern = r"(?P<boxes>^#.+#$)|(?P<directions>[<^>v]+)"
    # matches = re.findall(pattern, data, re.MULTILINE)

    matches = re.finditer(pattern, data, re.MULTILINE)

    # result = [match.groupdict() for match in matches]
    
    # print(result)

    # for match_index in range(len(matches) - 1):
    for match in matches:
        if match.groupdict()["boxes"]:
            lines.append(match.groupdict()["boxes"])
        # match = matches[match_index]
            print(f"matched boxes!: {match.groupdict()["boxes"]}")
        if match.groupdict()["directions"]:
            direction_string += match.groupdict()["directions"]
            print(f"matched direction!: {match.groupdict()["directions"]}")

positions = [[] for _ in range(len(lines))]
directions = []
x = 0
y = 0
robot_pos = [-1, -1]
wall_positions = []
box_positions = []
# print(positions)
for line in lines:
    x = 0
    for char in line:
        int_code = -1
        match char:
            case ".":
                int_code = 0
            case "#":
                int_code = 1
                wall_positions.append([x, y])
            case "O":
                int_code = 2
                box_positions.append([x, y])
            case "@":
                int_code = 3
                robot_pos = [x, y]
        positions[y].append(int_code)
        x += 1
    y += 1

for p in positions:
    print(p)

for dir in direction_string:
    match dir:
        case ">":
            int_code = 0
        case "v":
            int_code = 1
        case "<":
            int_code = 2
        case "^":
            int_code = 3
    directions.append(int_code)

dirs = [[1, 0], [0, 1], [-1, 0], [0, -1]]

print(f"\nrobot_pos: {robot_pos}")

for dir_code in directions:
    dir = dirs[dir_code]
    # print_i(f"dir: {dir_code} = {dir}")
    print_i(f"dir: {dir_code}")
    test_pos = [robot_pos[0] + dir[0], robot_pos[1] + dir[1]]
    test_char = positions[test_pos[1]][test_pos[0]]
    if test_char == 0:
        print_i("moved to empty spot")
        positions[robot_pos[1]][robot_pos[0]] = 0 # old robot spot
        positions[test_pos[1]][test_pos[0]] = 3 # new robot spot
        robot_pos = test_pos
    elif test_char == 1:
        print_i("hit a wall")
        # main(robot_pos, wall_positions, box_positions)
        continue
    # hit a box
    elif test_char == 2:
        print_i("hit a box")
        look_index = 1
        hit_wall = False
        boxes_to_push = [test_pos]
        while True:
            look_ahead_coord = [test_pos[0] + dir[0] * look_index, test_pos[1] + dir[1] * look_index]
            # hit a wall
            if positions[look_ahead_coord[1]][look_ahead_coord[0]] == 1:
                print_i("\thit a wall")
                hit_wall = True
                break
            
            # empty space so robot can move forward
            elif positions[look_ahead_coord[1]][look_ahead_coord[0]] == 0:
                print_i(f"\tmoved {len(boxes_to_push)} into an empty space")
                hit_wall = False
                break

            # hit another box which may or may not need to be later moved
            elif positions[look_ahead_coord[1]][look_ahead_coord[0]] == 2:
                boxes_to_push.append(look_ahead_coord)
            look_index += 1
        
        if not hit_wall:
            boxes_to_push.reverse()
            # for box_coords in boxes_to_push:
            #     new_coords = [box_coords[0] + dir[0], box_coords[1] + dir[1]]
            #     positions[new_coords[1]][new_coords[0]] = 2

            first_box_pushed_pos = [boxes_to_push[-1][0], boxes_to_push[-1][1]]
            last_box_pushed_pos = [boxes_to_push[0][0], boxes_to_push[0][1]]
            box_positions.append([last_box_pushed_pos[0] + dir[0], last_box_pushed_pos[1] + dir[1]])
            positions[last_box_pushed_pos[1] + dir[1]][last_box_pushed_pos[0] + dir[0]] = 2

            positions[robot_pos[1]][robot_pos[0]] = 0 # old robot spot
            robot_pos = first_box_pushed_pos
            box_positions.remove(first_box_pushed_pos)
            positions[first_box_pushed_pos[1]][first_box_pushed_pos[0]] = 3 # new robot spot
        else:
            # main(robot_pos, wall_positions, box_positions)
            continue
    # main(robot_pos, wall_positions, box_positions)
    # break
main(robot_pos, wall_positions, box_positions)

print("\n\n\n")
for p in positions:
    print(p)
print(f"\ndirections: {directions}")
x = 0
y = 0
for line in positions:
    x = 0
    for char in line:
        if char == 2:
            final_answer += 100 * y + x
        x += 1
    y += 1

print(final_answer) 
# final answer: 1514333