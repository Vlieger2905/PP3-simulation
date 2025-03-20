import math
import numpy as np
import pygame
import Setting
#Casper was here
# Class to define simulate the lidar scanner in the simulation
class Lidar():
    def __init__(self,position,direction):
        self.sensor_lines = Setting.laser_lines
        self.min_dist = Setting.lidar_min_dist
        self.max_dist = Setting.lidar_max_dist
        self.lasers = self.create_line(position, direction)

    def create_line(self, position, direction):
        sensory_lines = []
        # Normalize the direction vector
        magnitude = np.sqrt(direction[0]**2 + direction[1]**2)
        unit_vector = (direction[0] / magnitude, direction[1] / magnitude)

        # Loop through the sensor lines, ensuring the first line aligns with the direction
        for i in range(int(self.sensor_lines)):
            # Calculate the angle offset from the direction
            angle_offset = (i * (2 * math.pi / self.sensor_lines))
            # Rotate the direction vector by the angle offset
            dx_rot = np.cos(angle_offset) * unit_vector[0] - np.sin(angle_offset) * unit_vector[1]
            dy_rot = np.sin(angle_offset) * unit_vector[0] + np.cos(angle_offset) * unit_vector[1]
            # Scale to length and calculate the endpoint
            endpoint = (position[0] + self.max_dist * dx_rot, position[1] + self.max_dist * dy_rot)
            # Add the line to the list
            sensory_lines.append((endpoint, i))

        return sensory_lines

    def draw_lines(self,surface,position):
        for line in self.lasers:
            pygame.draw.line(surface,(255,0,0),position,line[0])
        pygame.draw.line(surface,(0,255,0),position, self.lasers[0][0])

    # Function to change the length of the sensory lines to either the detection range if there is not an obstacle in the way. Or to the side of the closest obstacle.
    def obstacle_detection(self, obstacles, car_position):
        index = 0
        # for each sensor line check whether they collide with any object
        for line in self.lasers:
            updated = False
            for object in obstacles:
                # If the line has been updated atleast once first check wether the new rect to collide with is within the new range of the newly created line
                if updated == True:
                    if math.dist(car_position,object.center)> new_line_dist:
                        continue
                
                # Save the result in endpoint
                end_point = self.collide_detect(line, object,car_position)
            
                # If there is a collision update the line to the new line
                if end_point != None:
                    new_line = (end_point, line[1])
                    new_line_dist = math.dist(car_position, new_line[0])
                    updated = True
            # Change the previouos line with the current one.
            if updated:
                self.lasers[index] = new_line
            index += 1
    
    # Function to check whether the line overlaps with a rectangle and return the closest position
    def collide_detect(self, line, obstacle,car_positioin):
        # Use clipline to check for collision
        clipped_line = obstacle.clipline(car_positioin, line[0])

        if clipped_line:
            # If clipped_line is not an empty tuple, then the line collides/overlaps with the rect
            start, end = clipped_line
            return start  # Return the first point where the line intersects with the rect
        else:
            return None  # Return None if no collision is detected