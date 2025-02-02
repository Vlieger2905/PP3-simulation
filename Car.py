import pygame
import math
import numpy as np
import Setting
import Lidar

class Car():
    def __init__(self,spawn):
        # Variables for pygame aspects
        self.spawn = spawn
        # Location of the car is the center of the car.
        self.position = spawn
        self.direction = pygame.Vector2(1,1)
        self.speed = 1
        self.rotation = self.direction
        # Lidar of the car
        self.lidar = Lidar.Lidar(self.position,self.direction)

    
    # Function to draw a rect where the position is the center of the car.
    def draw(self, surface):
        corners = self.rectangle_corners(self.position, Setting.car_width * 100, Setting.car_length * 100, (self.direction.x,self.direction.y))
        # Testing to draw a polygon instead of cars.
        pygame.draw.polygon(surface,(0,0,255),corners)

    # Function to move the car
    def move(self):
        self.position = self.position + self.direction * self.speed

    def update_car_rotation(self, steering_angle, delta_time = 1):
        # Calculate the turning radius using Ackermann steering geometry
        turning_radius = Setting.car_wheelbase / math.tan(math.radians(steering_angle))

        # Angular velocity: the car's speed along the arc of the turning circle
        angular_velocity = 1 / turning_radius  # Assuming unit speed for simplicity

        self.direction = pygame.Vector2.rotate(self.direction,angular_velocity)

    # Function to calculate the corners of the rectangle
    def rectangle_corners(self, center, width, length, direction):
        cx, cy = center
        dx, dy = direction[0],direction[1]

        # Normalize the direction vector
        magnitude = np.sqrt(dx**2 + dy**2)
        unit_vector = (dx / magnitude, dy / magnitude)
        
        # Perpendicular vector to direction
        perp_vector = (-unit_vector[1], unit_vector[0])
        
        # Half dimensions
        half_length = length / 2
        half_width = width / 2
        
        # Calculate corner offsets
        corners = [
            (cx + half_length * unit_vector[0] + half_width * perp_vector[0],  # Top-right
            cy + half_length * unit_vector[1] + half_width * perp_vector[1]),
            (cx + half_length * unit_vector[0] - half_width * perp_vector[0],  # Top-left
            cy + half_length * unit_vector[1] - half_width * perp_vector[1]),
            (cx - half_length * unit_vector[0] - half_width * perp_vector[0],  # Bottom-left
            cy - half_length * unit_vector[1] - half_width * perp_vector[1]),
            (cx - half_length * unit_vector[0] + half_width * perp_vector[0],  # Bottom-right
            cy - half_length * unit_vector[1] + half_width * perp_vector[1]),
        ]
        
        return corners


    # Function to update the car each frame
    def update(self, obstacles):
        # move the car
        self.move()
        # check collision

        # lidar scan if certain amount of time has passed
        self.lidar.lasers = self.lidar.create_line(self.position,self.direction)
        # 
        self.lidar.obstacle_detection(obstacles, self.position)
        # calculate the decision of the agent

        # execute the decision of the agent(rotate left, rotate right, brake, accelerate)
