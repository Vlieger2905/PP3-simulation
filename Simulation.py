import pygame
import sys
import numpy as np
import cupy as cp
import time
import Car, Map
import multiprocessing
import multiprocessing_test as mt
import populator as pop
import Setting as S

class Simulation:
    def __init__(self, amount_of_agents, start_position, start_direction):
        #Setting up the game class 
        self.screen = pygame.display.set_mode((S.WIDTH, S.HEIGTH))
        self.start_position = start_position
        # Setting up the fps control system of the game
        self.clock =  pygame.time.Clock()
        self.agents = []
        self.died_agents = []
        self.agent_sensory_lines = S.laser_lines
        # Creating the initial population of agents
        for i in range(amount_of_agents):
            self.agents.append(Car.Car(self.start_position, self.agent_sensory_lines, start_direction))
        # Map to train the cars on
        self.map = Map.Map()

    def Run(self, max_cores, agents_per_core, agents_multi_cutoff, simulation_length):
        steps = 0
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
            if self.agents.__len__() > agents_multi_cutoff and self.agents.__len__() > agents_per_core :
                cores = min(self.agents.__len__() // agents_per_core, max_cores)
                results = mt.multiprocess_lines(info, cores)
            
            elif self.agents.__len__() <= agents_multi_cutoff or self.agents.__len__() <= agents_per_core:
                results = [mt.collide_lines(*args) for args in info]

            # Index 0 = id, Index 1 = End position lidar lines, Index 2 = Distance to obstacle
            for i, item in enumerate(results):
                # Setting the lidar endpoints
                self.agents[i].lidar_endpoints =item[1]
                # Setting the distance to the obstacle
                self.agents[i].lidar = item[2]

            # Updating the agents
            self.update_agents()

            # Drawing the agents that are dead
            for agent in self.died_agents:
                agent.draw(self.screen, (255,0,0))

            steps += 1
            print("steps: ",steps)
            # If the simulation has run for the amount of steps or all agents are dead a new population gets made
            if steps == simulation_length or self.agents.__len__() == 0:
                # Adding all the died agents to the agents list
                self.agents.extend(self.died_agents)
                # Creating a new population based on the previous population
                self.agents = pop.procreation(self.agents)
                # Resetting the died agents and the steps
                self.died_agents = []
                steps = 0

            pygame.display.update()
            self.clock.tick()
    
    def update_agents(self):
        for agent in self.agents:
            # Letting the agent think about where to go
            agent.thinking(agent.lidar)

            # update the steering angle of movement
            if agent.decision == "full_left":
                agent.update_car_rotation(-S.max_steering_angle)
            elif agent.decision == "left":
                agent.update_car_rotation(-S.max_steering_angle/2)
            elif agent.decision == "center":
                pass
            elif agent.decision == "right":
                agent.update_car_rotation(S.max_steering_angle/2)
            elif agent.decision == "full_right":
                agent.update_car_rotation(S.max_steering_angle)

            # Moving the agent
            agent.move()
            
            # Check whether the car has collided with the wall
            for agent in self.agents:
                agent.update_car_outline()
                collided = agent.check_collision(self.map.rects)
                if collided:
                    self.died_agents.append(agent)
                    self.agents.remove(agent)
                else:
                    self.give_reward(agent)
                    
            # Drawing the agents
            for agent in self.agents:
                agent.draw(self.screen, agent.colour)

    # Function to give the agents rewards
    # Surviving one step gives a reward of 1
    #TODO More rewards should be added later.
    def give_reward(self,agent):
        # If the agent is still alive reward one point.
        agent.fitness += 1



