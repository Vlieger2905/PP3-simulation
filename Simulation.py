import pygame
import sys
import numpy as np
import Setting, Car, Map
import multiprocessing

class Simulation:
    def __init__(self):
        #Setting up the game class 
        self.screen = pygame.display.set_mode((Setting.WIDTH, Setting.HEIGTH))
        self.start_position = (640,370)
        # Setting up the fps control system of the game
        self.clock =  pygame.time.Clock()
        self.agents = []
        # temp to test car
        for i in range(400):
            self.agents.append(Car.Car(self.start_position))
        # Map to train the cars on
        self.map = Map.Map()

    def Run(self):
        i=0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            # Drawing the screen and updating it
            self.screen.fill("white")

            self.map.draw(self.screen)
            
            # Check if the D key is pressed
            keys = pygame.key.get_pressed()
            if keys[pygame.K_d]:
                self.agents[0].update_car_rotation(20)

            self.update_agents(self.agents)

            for agent in self.agents:
                agent.draw(self.screen)
                agent.lidar.draw_lines(self.screen, agent.position)
            # Updating the screen
            i += 1
            print(self.clock.get_fps())
            if i == 10000:
                quit()
            pygame.display.update()
            self.clock.tick()
    
    def update_agents(self, agents):
        for agent in agents:
            agent.update(self.map.rects)
