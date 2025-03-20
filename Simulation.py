import pygame
import sys
import numpy as np
import cupy as cp
import Setting, Car, Map
import multiprocessing
import multiprocessing_test as mt

class Simulation:
    def __init__(self, amount_of_agents):
        #Setting up the game class 
        self.screen = pygame.display.set_mode((Setting.WIDTH, Setting.HEIGTH))
        self.start_position = (640,370)
        # Setting up the fps control system of the game
        self.clock =  pygame.time.Clock()
        self.agents = []
        self.died_agents = []
        self.agent_sensory_lines = 16
        # temp to test car
        for i in range(amount_of_agents):
            self.agents.append(Car.Car(self.start_position, self.agent_sensory_lines))
        # Map to train the cars on
        self.map = Map.Map()

    def Run(self, cores):
        i=0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            # Drawing the screen and updating it
            self.screen.fill("white")

            self.map.draw(self.screen)
            
            # Creating the lidar lines for each agent
            for id, agent in enumerate(self.agents):
                agent.lidar = mt.create_lines(agent.position, agent.direction,self.agent_sensory_lines)

            # Get a list of distances and directions for each agent.
            info = [(id, agent.position,agent.lidar, self.map.rects) for  id, agent in enumerate(self.agents)]
            results = mt.multiprocess_lines(info, cores)
            # Index 0 = id, Index 1 = End position lidar lines, Index 2 = Distance to obstacle
            for id, item in enumerate(results):
                # Setting the lidar endpoints
                self.agents[id].lidar_endpoints =item[1]
                # Setting the distance to the obstacle
                self.agents[id].lidar = item[2]



            # Updating the agents
            self.update_agents()

            # Updating the screen
            i += 1
            # Printing FPS
            print(self.clock.get_fps())

            if i == 100:
                quit()
            pygame.display.update()
            self.clock.tick()
    
    def update_agents(self):
        for agent in self.agents:
            # Letting the agent think about where to go
            agent.thinking(agent.lidar)

            # update the steering angle of movement
            if agent.decision == "full_left":
                agent.update_car_rotation(-Setting.max_steering_angle)
            elif agent.decision == "left":
                agent.update_car_rotation(-Setting.max_steering_angle/2)
            elif agent.decision == "center":
                pass
            elif agent.decision == "right":
                agent.update_car_rotation(Setting.max_steering_angle/2)
            elif agent.decision == "full_right":
                agent.update_car_rotation(Setting.max_steering_angle)

            # Moving the agent
            agent.move()

            # Drawing the agent on the screen
            first = True
            for agent in self.agents:
                agent.draw(self.screen)
                # Drawing all the lidar lines of the first agent
                if first:
                    for line in agent.lidar_endpoints:
                        pygame.draw.line(self.screen, (255,0,0), agent.position, line[0])
                    first = False
            
            # Check whether the car has collided with the wall
            for agent in self.agents:
                collided = agent.check_collision(self.map.rects)
                if collided:
                    self.died_agents.append(agent)
                    self.agents.remove(agent)
                    


