import math, pandas
import numpy as np
import pygame
import Setting


class Map:
    def __init__(self):
        self.grid = pandas.read_csv(Setting.map_file)
        self.grid = self.grid.to_numpy()
        print(self.grid.shape)
        self.grid = np.transpose(self.grid)
        self.rects = self.create_rect()
        self.checkpoints = self.create_checkpoints()

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
        print(f"Created {len(collision_rects)} collision rects.")
        collision_rects = self.merge_rects(collision_rects)
        print(f"Merged into {len(collision_rects)} collision rects.")
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

    def create_checkpoints(self):
        checkpoints = []
        for checkpoint in Setting.checkpoints:
            start = checkpoint[0]
            end = checkpoint[1]
            start = (start[0] * Setting.grid_size, start[1] * Setting.grid_size)
            end = (end[0] * Setting.grid_size, end[1] * Setting.grid_size)
            checkpoints.append((start,end))
        return checkpoints



    # drawing the map on the screen
    def draw(self,surface, offset):
        # Drawing the walls
        for rect in self.rects:
            pygame.draw.rect(surface, (0, 0, 0), pygame.Rect(rect.left + offset[0], rect.top + offset[1], rect.width, rect.height))
        # Drawing the checkpoints
        for checkpoint in self.checkpoints:
            pygame.draw.line(surface, (0,255,0), (int(checkpoint[0][0] + offset[0]), int(checkpoint[0][1] + offset[1])), (int(checkpoint[1][0] + offset[0]), int(checkpoint[1][1] + offset[1])))

    def lines_collide(self, line1, line2):
        def ccw(A, B, C):
            # Check if three points are listed in a counterclockwise order
            return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])

        A, B = line1  # Start and end points of the first line
        C, D = line2  # Start and end points of the second line

        # Lines collide if the endpoints are in different orientations relative to each other
        return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)