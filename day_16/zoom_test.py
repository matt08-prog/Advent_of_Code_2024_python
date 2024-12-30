import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pan and Zoom Example")

# Load an image (replace with your own image path)
original_image = pygame.image.load("test_image.jpg").convert()
image = original_image.copy()

# Initial position and zoom level
pos_x, pos_y = 0, 0
zoom = 1.0
zoom_speed = 0.1

# Main game loop
running = True
panning = False
pan_start_pos = None

clock = pygame.time.Clock()

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

    # Calculate the size and position of the zoomed image
    zoomed_size = (int(image.get_width() * zoom), int(image.get_height() * zoom))
    zoomed_image = pygame.transform.scale(original_image, zoomed_size)

    # Blit the zoomed image onto the screen
    screen.blit(zoomed_image, (pos_x, pos_y))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
