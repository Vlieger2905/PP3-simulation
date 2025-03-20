import pygame
import math, random
import numpy as np
import Setting
import Lidar
from Neural.Brain import Brain
#Casper was here
class Car():
    def __init__(self,spawn, lidar_amount):
        # Variables for pygame aspects
        self.spawn = spawn
        # Location of the car is the center of the car.
        self.position = spawn
        angle = random.uniform(0, 2 * math.pi)
        self.direction = pygame.Vector2(math.cos(angle), math.sin(angle))
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
        self.brain = Brain(lidar_amount)

    
    # Function to draw a rect where the position is the center of the car.
    def draw(self, surface):
        self.corners = self.rectangle_corners(self.position, Setting.car_width * 100, Setting.car_length * 100, (self.direction.x,self.direction.y))
        # Testing to draw a polygon instead of cars.
        pygame.draw.polygon(surface,(0,0,255),self.corners)

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

    # Function to check whether the car is colliding with the wall
    def check_collision(self, walls):
        for wall in walls:
            distance = math.dist(wall.center, self.position)
            if distance < int(Setting.car_length * 10):
                for corner in self.corners:
                    if wall.collidepoint(corner):
                        return True
        return False


    def thinking(self, input):
        self.decision = self.brain.thinking(input)
