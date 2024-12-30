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
    global positions
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
        if positions[y][x] == 4:
            pygame.draw.rect(SCREEN, (50,50,50), (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        elif  positions[y][x] == 5:
            pygame.draw.rect(SCREEN, (150,150,150), (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        else:
            print_i(f"missing box at {[x, y]}")
            exit(-1)


    
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
debug = False

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
        int_codes = [-1, -1]
        match char:
            case ".":
                int_codes = [0, 0]
            case "#":
                int_codes = [1, 1]
                wall_positions.append([x, y])
                wall_positions.append([x + 1, y])
            case "O":
                int_codes = [4, 5]
                box_positions.append([x, y])
                box_positions.append([x + 1, y])
            case "@":
                int_codes = [3, 0]
                robot_pos = [x, y]
        positions[y].append(int_codes[0])
        positions[y].append(int_codes[1])
        x += 2
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
    if debug:
        main(robot_pos, wall_positions, box_positions)
    dir = dirs[dir_code]
    # print_i(f"dir: {dir_code} = {dir}")
    test_pos = [robot_pos[0] + dir[0], robot_pos[1] + dir[1]]
    test_char = positions[test_pos[1]][test_pos[0]]
    print_i(f"dir: {dir_code}; testing: {test_pos} = {test_char}", 1)
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
    elif test_char == 4 or test_char == 5:
        print_i("hit a box")
        look_index = 1
        hit_wall = False
        # boxes_to_push = [test_pos]
        boxes_to_push = []
        up_down = dir_code == 1 or dir_code == 3
        poses_to_check = []
        if up_down:
            if test_char == 4:
                poses_to_check.append([test_pos[0] + dir[0], test_pos[1] + dir[1]])
                poses_to_check.append([test_pos[0] + dir[0] + 1, test_pos[1] + dir[1]])
                
                left_pos = [test_pos[0], test_pos[1]]
                right_pos = [test_pos[0] + 1, test_pos[1]]
                if left_pos not in boxes_to_push:
                    boxes_to_push.append(left_pos)
                if right_pos not in boxes_to_push:
                    boxes_to_push.append(right_pos)
            elif test_char == 5:
                poses_to_check.append([test_pos[0] + dir[0], test_pos[1] + dir[1]])
                poses_to_check.append([test_pos[0] + dir[0] - 1, test_pos[1] + dir[1]])

                # boxes_to_push.append([test_pos[0], test_pos[1]])
                # boxes_to_push.append([test_pos[0] - 1, test_pos[1]])
                right_pos = [test_pos[0], test_pos[1]]
                left_pos = [test_pos[0] - 1, test_pos[1]]
                if left_pos not in boxes_to_push:
                    boxes_to_push.append(left_pos)
                if right_pos not in boxes_to_push:
                    boxes_to_push.append(right_pos)
        elif not up_down:
            poses_to_check.append([test_pos[0] + dir[0] * 2, test_pos[1] + dir[1]])

            # boxes_to_push.append([test_pos[0], test_pos[1]])
            # boxes_to_push.append([test_pos[0] + dir[0], test_pos[1]])
            first_pos = [test_pos[0], test_pos[1]]
            second_pos = [test_pos[0] + dir[0], test_pos[1]]
            if first_pos not in boxes_to_push:
                boxes_to_push.append(first_pos)
            if second_pos not in boxes_to_push:
                boxes_to_push.append(second_pos)
        hit_one_or_more_boxes = False
        # row_index = 0
        while len(poses_to_check) > 0:
            pos_to_check = poses_to_check[0]
            # look_ahead_coord = [test_pos[0] + dir[0] * look_index, test_pos[1] + dir[1] * look_index]
            look_ahead_coord = pos_to_check
            print_i(f"\t\thit a box, now testing: {pos_to_check} = {positions[look_ahead_coord[1]][look_ahead_coord[0]]}", 1)
            
            # hit a wall
            if positions[look_ahead_coord[1]][look_ahead_coord[0]] == 1:
                print_i("\thit a wall")
                hit_wall = True
                break
            
            # empty space so robot can move forward
            elif positions[look_ahead_coord[1]][look_ahead_coord[0]] == 0:
                print_i(f"\tmoved {len(boxes_to_push)} into an empty space")
                hit_wall = False
                poses_to_check.remove(pos_to_check)
                # break
            elif up_down:
                # hit another box which may or may not need to be later moved
                if positions[look_ahead_coord[1]][look_ahead_coord[0]] == 4:
                    left_pos = [look_ahead_coord[0], look_ahead_coord[1]]
                    right_pos = [look_ahead_coord[0] + 1, look_ahead_coord[1]]

                    new_left_check = [left_pos[0], left_pos[1] + dir[1]]
                    new_right_check = [right_pos[0], right_pos[1] + dir[1]]
                    if new_left_check not in poses_to_check:
                        poses_to_check.append(new_left_check)
                    if new_right_check not in poses_to_check:
                        poses_to_check.append(new_right_check)

                    if left_pos not in boxes_to_push:
                        print_i(f"7added {left_pos} to {boxes_to_push}")
                        boxes_to_push.append(left_pos)
                    if right_pos not in boxes_to_push:
                        print_i(f"8added {right_pos} to {boxes_to_push}")
                        boxes_to_push.append(right_pos)
                    poses_to_check.remove(pos_to_check)
                    hit_one_or_more_boxes = True
                # hit another box which may or may not need to be later moved
                if positions[look_ahead_coord[1]][look_ahead_coord[0]] == 5:
                    right_pos = [look_ahead_coord[0], look_ahead_coord[1]]
                    left_pos = [look_ahead_coord[0] - 1, look_ahead_coord[1]]

                    new_left_check = [left_pos[0], left_pos[1] + dir[1]]
                    new_right_check = [right_pos[0], right_pos[1] + dir[1]]
                    if new_left_check not in poses_to_check:
                        poses_to_check.append(new_left_check)
                    if new_right_check not in poses_to_check:
                        poses_to_check.append(new_right_check)
                    
                    if left_pos not in boxes_to_push:
                        print_i(f"9added {left_pos} to {boxes_to_push}")
                        boxes_to_push.append(left_pos)
                    if right_pos not in boxes_to_push:
                        print_i(f"10added {right_pos} to {boxes_to_push}")
                        boxes_to_push.append(right_pos)
                    poses_to_check.remove(pos_to_check)
                    hit_one_or_more_boxes = True
            elif not up_down:
                first_pos = [look_ahead_coord[0], look_ahead_coord[1]]
                second_pos = [look_ahead_coord[0] + dir[0], look_ahead_coord[1]]

                new_check = [look_ahead_coord[0] + dir[0] * 2, look_ahead_coord[1]]
                if new_check not in poses_to_check:
                    poses_to_check.append(new_check)

                if first_pos not in boxes_to_push:
                    print_i(f"11added {first_pos} to {boxes_to_push}")
                    boxes_to_push.append(first_pos)
                if second_pos not in boxes_to_push:
                    print_i(f"12added {second_pos} to {boxes_to_push}")
                    boxes_to_push.append(second_pos)
                poses_to_check.remove(pos_to_check)
            # look_index += 1 + int(not up_down)
            # look_index += 1
        
        if not hit_wall:
            boxes_to_push.reverse()

            first_box_pushed_pos = [boxes_to_push[-1][0], boxes_to_push[-1][1]]
            last_box_pushed_pos = [boxes_to_push[0][0], boxes_to_push[0][1]]
            print_i(f"list of boxes to be pushed: {boxes_to_push}")
            print_i(f"\tcurrent box positions: {box_positions}")

            for box_coords in boxes_to_push:
                old_char = positions[box_coords[1]][box_coords[0]]
                new_coords = [box_coords[0] + dir[0], box_coords[1] + dir[1]]
                positions[new_coords[1]][new_coords[0]] = old_char # moved to position
                positions[box_coords[1]][box_coords[0]] = 0 # old position
                box_positions.remove(box_coords)
                box_positions.append(new_coords)

            # box_positions.append([last_box_pushed_pos[0] + dir[0], last_box_pushed_pos[1] + dir[1]])
            # positions[last_box_pushed_pos[1] + dir[1]][last_box_pushed_pos[0] + dir[0]] = 2 #  needs to change

            positions[robot_pos[1]][robot_pos[0]] = 0 # old robot spot
            # robot_pos = first_box_pushed_pos
            robot_pos = test_pos
            # box_positions.remove(first_box_pushed_pos)
            positions[test_pos[1]][test_pos[0]] = 3 # new robot spot
        else:
            # main(robot_pos, wall_positions, box_positions)
            continue
    # main(robot_pos, wall_positions, box_positions)
    # break
if not debug:
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
        if char == 4:
            final_answer += 100 * y + x
        x += 1
    y += 1

print(final_answer) 
# final answer: 1528453