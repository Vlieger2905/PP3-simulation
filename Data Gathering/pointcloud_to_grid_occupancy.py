import numpy as np
import pygame
import csv


with open("Data Gathering/final_map.txt", "r") as f:
    lines = f.readlines()
    points = []
    for line in lines:
        x, y = map(float, line.split())
        points.append((x, y))
# Change the cube size to the size of the grid 
def pointcloud_to_grid(points, cube_size=10):
    # Extract x and y coordinates
    x_coords = [p[0] for p in points]
    y_coords = [p[1] for p in points]

    # Determine the grid dimensions
    min_x, max_x = min(x_coords), max(x_coords)
    min_y, max_y = min(y_coords), max(y_coords)

    grid_width = int(np.ceil((max_x - min_x) / cube_size))
    grid_height = int(np.ceil((max_y - min_y) / cube_size))

    # Initialize the grid with zeros
    grid = np.zeros((grid_height, grid_width), dtype=int)

    # Populate the grid
    for x, y in points:
        grid_x = int((x - min_x) // cube_size)
        grid_y = int((y - min_y) // cube_size)

        # Clamp indices to ensure they are within bounds
        grid_x = min(grid_x, grid_width - 1)
        grid_y = min(grid_y, grid_height - 1)

        grid[grid_y, grid_x] = 1

    return grid

# Example usage

grid = pointcloud_to_grid(points)

def save_grid_to_file(grid, filename="grid_output.csv"):
    with open(filename, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(grid)

# Save the grid to a file
save_grid_to_file(grid)

pygame.init()
screen = pygame.display.set_mode((1000, 1000))
clock = pygame.time.Clock()
screen.fill((255, 255, 255))
cubes = []
cube_size = 2
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[i, j] == 1:
                cube = pygame.Rect(j * cube_size, i * cube_size, cube_size, cube_size)
                cubes.append(cube)
                pygame.draw.rect(screen, (0, 0, 0), cube)
    pygame.display.flip()
