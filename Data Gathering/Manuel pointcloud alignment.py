import math
import pygame
import numpy as np
import os


path = "Data Gathering\Data gathering\Converted Data"
files = os.listdir(path)
# Sort files numerically based on the number in the filename
files = sorted(files, key=lambda x: int(''.join(filter(str.isdigit, x))))
# putting the xyz data into point clouds
point_clouds = []
for i, file in enumerate(files):
    with open(os.path.join(path, file), "r") as f:
        lines = f.readlines()
        points = []
        for line in lines:
            x, y,z = map(float, line.split())
            points.append((x, y,z))
        point_clouds.append(np.array(points))  

print(f"Loaded {len(point_clouds)} point clouds.")

pygame.init()
screen = pygame.display.set_mode((2560,1600))
clock = pygame.time.Clock()

grid_size = 5
grid = np.zeros((int(2560/grid_size), int(1600/grid_size)))
point_cloud_counter = 0
center_y = 2560/2
center_x = 1600/2
final_x = 0
final_y = 0
speed = 1

# Pointcloud to save final map result
final_map = []
final_map_location = "Data Gathering"

# Each pixel is a distance of 1 cm and the grid size is 5 cm. therfore the value of the pixels is devided by 10
rescale_factor = 10
# Program loop to display the point clouds
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
            if event.key == pygame.K_m:
                with open(os.path.join(final_map_location, "final_map.txt"), "w") as f:
                    for point in final_map:
                        f.write(f"{point[0]} {point[1]}\n")
                print("Final map saved to final_map.txt.")
                pygame.quit()
                exit()


    screen.fill((255, 255, 255))  # Set screen color to white

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        center_y -= speed
    if keys[pygame.K_s]:
        center_y += speed
    if keys[pygame.K_a]:
        center_x -= speed
    if keys[pygame.K_d]:
        center_x += speed
    # Moving the final map up and down
    if keys[pygame.K_UP]:
        final_y -=speed
    if keys[pygame.K_DOWN]:
        final_y +=speed
    if keys[pygame.K_LEFT]:
        final_x -=speed
    if keys[pygame.K_RIGHT]:
        final_x +=speed

    # Increasing the speed
    if keys[pygame.K_LSHIFT]:
        speed =5
    else:
        speed = 1

    # Rotate the current point cloud
    if keys[pygame.K_e]:  # Rotate clockwise
        rotation_matrix = np.array([
            [math.cos(math.radians(1)), -math.sin(math.radians(1)), 0],
            [math.sin(math.radians(1)), math.cos(math.radians(1)), 0],
            [0, 0, 0.1]
        ])
        point_clouds[point_cloud_counter] = np.dot(point_clouds[point_cloud_counter], rotation_matrix.T)

    if keys[pygame.K_q]:  # Rotate counterclockwise
        rotation_matrix = np.array([
            [math.cos(math.radians(-1)), -math.sin(math.radians(-1)), 0],
            [math.sin(math.radians(-1)), math.cos(math.radians(-1)), 0],
            [0, 0, 0.1]
        ])
        point_clouds[point_cloud_counter] = np.dot(point_clouds[point_cloud_counter], rotation_matrix.T)

    # Draw the current point cloud
    for point in point_clouds[point_cloud_counter]:
        screen_x = int(center_x + int(point[0]/rescale_factor))
        screen_y = int(center_y + int(point[1]/rescale_factor))  # Invert y-axis for screen coordinates
        pygame.draw.circle(screen, (0, 0, 0), (screen_x, screen_y), 1)

    for point in final_map:
        screen_x = int(final_x + point[0])
        screen_y = int(final_y + point[1]) 
        pygame.draw.circle(screen, (255, 0, 0), (screen_x, screen_y), 1)

    # Saving the current point cloud to the final map
    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:  # Check if the Enter key is pressed
        if not hasattr(event, 'handled') or not event.handled:  # Ensure it triggers only once
            for point in point_clouds[point_cloud_counter]:
                screen_x = int(center_x - final_x + int(point[0]/rescale_factor))
                screen_y = int(center_y - final_y + int(point[1]/rescale_factor))
                final_map.append((screen_x, screen_y))  # Save the point in the final map
            point_cloud_counter += 1
            print(f"Point cloud {point_cloud_counter} saved to final map.")
            event.handled = True

        if point_cloud_counter >= len(point_clouds):
            point_cloud_counter = 0
    
    
    if event.type == pygame.KEYUP and event.key == pygame.K_RETURN:  # Reset when the Enter key is released
        event.handled = False

    pygame.display.flip()  # Correctly update the display
    clock.tick(10)  # Set the frame rate to 60 FPS
