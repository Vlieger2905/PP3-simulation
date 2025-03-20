import pygame
import random
import sys
import numpy as np
import math, time
import Setting
import multiprocessing
# Initialize pygame
pygame.init()
#Casper was not here, but Wouter was.
def create_lines(position, direction, amount_of_lines):
        sensory_lines = []
        sensor_lines = amount_of_lines
        # Normalize the direction vector
        magnitude = np.sqrt(direction[0]**2 + direction[1]**2)
        unit_vector = (direction[0] / magnitude, direction[1] / magnitude)

        # Loop through the sensor lines, ensuring the first line aligns with the direction
        for i in range(int(sensor_lines)):
            # Calculate the angle offset from the direction
            angle_offset = (i * (2 * math.pi / sensor_lines))
            # Rotate the direction vector by the angle offset
            dx_rot = np.cos(angle_offset) * unit_vector[0] - np.sin(angle_offset) * unit_vector[1]
            dy_rot = np.sin(angle_offset) * unit_vector[0] + np.cos(angle_offset) * unit_vector[1]
            # Scale to length and calculate the endpoint
            endpoint = (position[0] + 1000 * dx_rot, position[1] + 1000 * dy_rot)
            # Add the line to the list
            sensory_lines.append((endpoint, i))

        return sensory_lines

def collide_lines(id, position, lines, rects):
    index = 0
    distance = []
    for line in lines:
        updated = False
        for object in rects:
            # If the line has been updated atleast once first check wether the new rect to collide with is within the new range of the newly created line
            if updated == True:
                if math.dist(position,object.center)> new_line_dist:
                    continue
            
            # Save the result in endpoint
            end_point = collide_detect(line, object, position)
        
            # If there is a collision update the line to the new line
            if end_point != None:
                new_line = (end_point, line[1])
                new_line_dist = math.dist(position, new_line[0])
                updated = True
        # Change the previouos line with the current one.
        if updated:
            lines[index] = new_line
        distance.append(math.dist(position, lines[index][0]))
        index += 1
    return (id, lines, distance)
         
def create_rects(Max_rexts):
    x_min, x_max = 0,1000
    y_min, y_max = 0, 720  
    rect_size = 10
    rects = []
    for i in range(Max_rexts):
        x_pos = random.randint(x_min,x_max)
        y_pos = random.randint(y_min,y_max)
        rects.append(pygame.Rect(x_pos,y_pos, rect_size, rect_size))
    return rects

def collide_detect(line, obstacle, car_positioin):
        # Use clipline to check for collision
        clipped_line = obstacle.clipline(car_positioin, line[0])

        if clipped_line:
            # If clipped_line is not an empty tuple, then the line collides/overlaps with the rect
            start, end = clipped_line
            return start  # Return the first point where the line intersects with the rect
        else:
            return None  # Return None if no collision is detected
# Wrapper to unpack all the information into one tuple
def collide_lines_wrapper(args):
    return collide_lines(*args)

# def multiprocess_lines(agents, rects, processes):
#     pool = multiprocessing.Pool(processes=processes)
#     arguments = [(id, agent[0],agent[1], rects) for  id, agent in enumerate(agents)]
#     results = pool.map(collide_lines_wrapper, arguments)
#     return results

def multiprocess_lines(arguments, processes):
    pool = multiprocessing.Pool(processes=processes)
    results = pool.map(collide_lines_wrapper, arguments)
    return results


def main():
    rects = create_rects(1000)
    agents =[]
    number_of_agents = 400
    for i in range(number_of_agents):
        x_pos, y_pos = random.randint(100, 900),random.randint(100, 900)
        agents.append(((x_pos,y_pos),create_lines((x_pos, y_pos), (0,1))))

    # loop running
    screen = pygame.display.set_mode((Setting.WIDTH, Setting.HEIGTH))
    i=0
    start_time = time.time()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        # Drawing the screen and updating it
        screen.fill("white")

        results = multiprocess_lines(agents, rects, 6)
        # This can be used to do the exact same step without the multiprocessing
        # arguments = [(id, agent[0],agent[1], rects) for  id, agent in enumerate(agents)]
        # for argument in arguments:
        #     results = collide_lines_wrapper(argument)

        # Updating the screen
        i += 1
        if i == 100:
            total_time = time.time() - start_time
            print(total_time)
            quit()
        pygame.display.update()

if __name__ == '__main__':
    # Wrap your main loop with cProfile3
    main()  