import pygame
import math, random
import numpy as np
import Setting
import Lidar
from Neural.Brain import Brain
#Casper was here
class Car():
    def __init__(self,spawn, lidar_amount, direction, checkpoints, Genes = None):
        # Variables for pygame aspects
        self.spawn = spawn
        self.colour = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        # Location of the car is the center of the car.
        self.position = spawn
        self.direction = pygame.Vector2(direction)
        self.direction = self.direction.normalize()
        self.speed = 18
        self.rotation = self.direction
        # Lidar of the car
        # Distance from lidar to obstacle
        self.lidar = []
        # Endpoints of the lines
        self.lidar_endpoints = []

        # Decision of the agent of where to go
        self.decision = "left"
        # Brain of the agent
        if Genes:
            pass
        else:
            self.brain = Brain(lidar_amount)
        # Fitness of the agent. Total rewards gained
        self.fitness = 0

        # Checkpoints that the agents has not yet hit
        self.checkpoints = checkpoints

        # Corners of the car and outline of the car
        self.corners = self.rectangle_corners(self.position, Setting.car_width * 100, Setting.car_length * 100, (self.direction.x,self.direction.y))
        self.outline = self.create_outline()

    # Function to draw the best car
    def best_draw(self, surface, offset, colour):
        # Apply the offset to the car's corners
        offset_corners = [(x + offset[0], y + offset[1]) for x, y in self.corners]
        # Draw the polygon of the car with the offset
        pygame.draw.polygon(surface, colour, offset_corners)

    # Function to draw the car
    def draw(self, surface, offset):
        # Apply the offset to the car's corners
        offset_corners = [(x + offset[0], y + offset[1]) for x, y in self.corners]
        # Draw the polygon of the car with the offset
        pygame.draw.polygon(surface, self.colour, offset_corners)

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
    
    # Create a list of lines that represent the outline of the car based on the corners of the car
    def create_outline(self):
        outline = []
        outline.append((self.corners[0], self.corners[1]))
        outline.append((self.corners[1], self.corners[2]))
        outline.append((self.corners[2], self.corners[3]))
        outline.append((self.corners[3], self.corners[0]))
        return outline

    def update_car_outline(self):
        self.corners = self.rectangle_corners(self.position, Setting.car_width * 100, Setting.car_length * 100, (self.direction.x,self.direction.y))
        self.outline = self.create_outline()

    # Function to check whether the car is colliding with the wall
    def check_collision(self, walls):
        for wall in walls:
            for line in self.outline:
                if wall.clipline(line):
                    return True
        return False

    def thinking(self, input):
        self.decision = self.brain.thinking(input)