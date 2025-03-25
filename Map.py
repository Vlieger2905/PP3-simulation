import math, pandas
import numpy as np
import pygame
import Setting


class Map:
    def __init__(self):
        self.grid = pandas.read_csv("oval_circuit_matrix.csv")
        self.grid = self.grid.to_numpy()
        self.grid = np.transpose(self.grid)
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
        # Merge the rects to reduce the amount of rects to collide with 
        collision_rects = self.merge_rects(collision_rects)
        return collision_rects
    
    def merge_rects(self, rects):
        if not rects:
            return []
        
        # Sort by y, then x to ensure order
        rects.sort(key=lambda r: (r.top, r.left))
        
        merged = []
        current = rects[0]
        
        # Merge horizontally adjacent rects
        for r in rects[1:]:
            if r.top == current.top and r.height == current.height and r.left == current.right:
                # Extend the width
                current.width += r.width
            else:
                merged.append(current)
                current = r
        merged.append(current)
        
        # Sort by x, then y for vertical merging
        merged.sort(key=lambda r: (r.left, r.top))
        final_merged = []
        current = merged[0]
        
        # Merge vertically adjacent rects
        for r in merged[1:]:
            if r.left == current.left and r.width == current.width and r.top == current.bottom:
                # Extend the height
                current.height += r.height
            else:
                final_merged.append(current)
                current = r
        final_merged.append(current)
        
        return final_merged

    # drawing the map on the screen
    def draw(self,surface,):
        for rect in self.rects:
            pygame.draw.rect(surface, (0,0,0),rect)
