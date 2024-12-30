import pygame
import sys
import numpy as np

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Grid Pan and Zoom Example")

# Create a 2D array of walls (1 for wall, 0 for empty)
GRID_SIZE = 50
walls = np.random.choice([0, 1], size=(GRID_SIZE, GRID_SIZE), p=[0.7, 0.3])

# Colors
WALL_COLOR = (100, 100, 100)  # Gray
EMPTY_COLOR = (255, 255, 255)  # White

# Initial position and zoom level
pos_x, pos_y = 0, 0
zoom = 10.0
zoom_speed = 0.1

# Main game loop
running = True
panning = False
pan_start_pos = None

clock = pygame.time.Clock()

def draw_grid():
    cell_size = zoom
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            rect = pygame.Rect(
                int(x * cell_size + pos_x),
                int(y * cell_size + pos_y),
                int(cell_size),
                int(cell_size)
            )
            color = WALL_COLOR if walls[y][x] == 1 else EMPTY_COLOR
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (0, 0, 0), rect, 1)  # Draw cell borders
            # print("drew rect")

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                panning = True
                pan_start_pos = event.pos
            elif event.button == 4:  # Scroll up
                # Calculate mouse position in image space
                mouse_x, mouse_y = event.pos
                img_x = (mouse_x - pos_x) / zoom
                img_y = (mouse_y - pos_y) / zoom
                
                # Zoom in
                zoom *= (1 + zoom_speed)
                
                # Adjust position to zoom towards mouse
                pos_x = mouse_x - img_x * zoom
                pos_y = mouse_y - img_y * zoom
            elif event.button == 5:  # Scroll down
                # Calculate mouse position in image space
                mouse_x, mouse_y = event.pos
                img_x = (mouse_x - pos_x) / zoom
                img_y = (mouse_y - pos_y) / zoom
                
                # Zoom out
                zoom /= (1 + zoom_speed)
                
                # Adjust position to zoom towards mouse
                pos_x = mouse_x - img_x * zoom
                pos_y = mouse_y - img_y * zoom
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button
                panning = False
        elif event.type == pygame.MOUSEMOTION:
            if panning:
                mouse_x, mouse_y = event.pos
                pos_x += mouse_x - pan_start_pos[0]
                pos_y += mouse_y - pan_start_pos[1]
                pan_start_pos = event.pos
    # Clear the screen
    screen.fill((0, 0, 0))

    draw_grid()

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)
