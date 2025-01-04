import math, pandas
import numpy as np
import pygame
import Setting


class Map:
    def __init__(self):
        # Create a grid filled with random 0s and 1s
        # self.grid = np.random.randint(2, size=(int(Setting.WIDTH / Setting.grid_size), int(Setting.HEIGTH / Setting.grid_size)))
        self.grid = pandas.read_csv("oval_circuit_matrix.csv")
        self.grid = self.grid.to_numpy()
        self.grid = self.grid.swapaxes(0,1)
        self.rects = self.create_rect()

    # Creating the rects to collide the lasers and cars with 
    def create_rect(self):
        collision_rects = []
        i = 0 
        j = 0
        for row in self.grid:
            for col in row:
                if col == 1:
                    collision_rects.append(pygame.Rect(i * Setting.grid_size, j * Setting.grid_size, Setting.grid_size, Setting.grid_size))
                j += 1
            i += 1
            j = 0
        return collision_rects
    
    # drawing the map on the screen
    def draw(self,surface,):
        for rect in self.rects:
            pygame.draw.rect(surface, (0,0,0),rect)

