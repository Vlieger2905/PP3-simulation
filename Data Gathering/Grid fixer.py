import pygame
import csv
import time

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
CUBE_SIZE = 10
GRID_COLOR = (200, 200, 200)
CUBE_COLOR = (0, 0, 255)
CHECKPOINT_COLOR = (255, 0, 0)

# Load CSV file and parse grid
def load_csv(file_path):
    grid = []
    checkpoints = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            line = []
            for cell in row:
                line.append(int(cell))  # Convert string to int
                if cell == '2':
                    checkpoints.append((len(grid), len(line) - 1))  # Store checkpoint position
            grid.append(line)
    return grid

# Save grid back to CSV
def save_csv(file_path, grid):
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(grid)

# Draw the grid
def draw_grid(screen, grid,offset_x, offset_y):
    # Draw the grid with offsets
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            # Drawing occupied cells
            if cell == 1:
                pygame.draw.rect(screen, CUBE_COLOR, ((x * CUBE_SIZE) + offset_x, (y * CUBE_SIZE) + offset_y, CUBE_SIZE, CUBE_SIZE))
            # Drawing checkpoints
            if cell == 2:
                pygame.draw.rect(screen, CHECKPOINT_COLOR, ((x * CUBE_SIZE) + offset_x, (y * CUBE_SIZE) + offset_y, CUBE_SIZE, CUBE_SIZE))
            pygame.draw.rect(screen, GRID_COLOR, (x * CUBE_SIZE, y * CUBE_SIZE, CUBE_SIZE, CUBE_SIZE), 1)


csv_file = "Data Gathering\Mapdata\map DB limited bounds 3 of 4 .csv"
# Main function
def main(csv_file = None, x= 300, y = 300):
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Grid Editor")

    # Load initial grid from CSV
    if csv_file:
        grid = load_csv(csv_file)
    else:
        # Create a new grid of specified dimensions
        grid = [[0 for _ in range(x)] for _ in range(y)]
        csv_file = f"{time.time()}.csv"

    running = True
    # Add WASD movement functionality
    offset_x, offset_y = 100,100  # Initialize offsets for grid movement
    move_speed = 10  # Speed of movement

    is_dragging = False  # Track if the mouse is being dragged
    drag_button = None  # Track which button is being dragged

    while running:
        screen.fill((255, 255, 255))

        # Draw the grid with offsets
        draw_grid(screen, grid, offset_x, offset_y)
       
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_csv(csv_file, grid)  # Save grid to CSV on exit
                pygame.quit()
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                is_dragging = True
                drag_button = event.button
                x, y = pygame.mouse.get_pos()
                grid_x = (x - offset_x) // CUBE_SIZE
                grid_y = (y - offset_y) // CUBE_SIZE

                # Ensure grid position is within bounds
                if 0 <= grid_y < len(grid) and 0 <= grid_x < len(grid[0]):
                    if drag_button == 1:  # Left mouse button
                        grid[grid_y][grid_x] = 1
                    elif drag_button == 3:  # Right mouse button
                        grid[grid_y][grid_x] = 0

            elif event.type == pygame.MOUSEBUTTONUP:
                is_dragging = False
                drag_button = None

            elif event.type == pygame.MOUSEMOTION and is_dragging:
                x, y = pygame.mouse.get_pos()
                grid_x = (x - offset_x) // CUBE_SIZE
                grid_y = (y - offset_y) // CUBE_SIZE

                # Ensure grid position is within bounds
                if 0 <= grid_y < len(grid) and 0 <= grid_x < len(grid[0]):
                    if drag_button == 1:  # Left mouse button
                        grid[grid_y][grid_x] = 1
                    elif drag_button == 3:  # Right mouse button
                        grid[grid_y][grid_x] = 0

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Space bar
                    x, y = pygame.mouse.get_pos()
                    grid_x = (x - offset_x) // CUBE_SIZE
                    grid_y = (y - offset_y) // CUBE_SIZE

                    # Ensure grid position is within bounds
                    print(f"x:{grid_x},y:{grid_y}")

        # Handle key presses for movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:  # Move up
            offset_y += move_speed
        if keys[pygame.K_s]:  # Move down
            offset_y -= move_speed
        if keys[pygame.K_a]:  # Move left
            offset_x += move_speed
        if keys[pygame.K_d]:  # Move right
            offset_x -= move_speed

        pygame.display.flip()
if __name__ == "__main__":
    main(csv_file)