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
        
        draw_grid(robot_pos, walls, boxes)
    
    pygame.quit()
    sys.exit()

def get_color(seed):
    random.seed(seed)
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

# if __name__ == "__main__":
#     main()



lines = []
final_answer = 1
input_file_name = "test_input_1.txt" # 140
# input_file_name = "test_input_2.txt" # 772
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
    pattern = r"((\n#(.+)#$)|(?P<directions>[<^>v]+))"
    matches = re.findall(pattern, data, re.MULTILINE)
    for match_index in range(len(matches) - 1):
        match = matches[match_index]
        print(f"matched!: {match}")
    # if match:
        # robot["pos"] = [int(match.group(1)), int(match.group(2))]
        # robot["vel"] = [int(match.group(3)), int(match.group(4))]
        # robot["quadrant"] = -1
        # robot = DotDict(robot)
        # print(robot.pos)
        # print(robot.vel)
        # robots.append(robot)


print("\n\n\n")

for robot in robots:
    print(robot)

print(final_answer) 
# 96165888 too low
# final answer: 218619324