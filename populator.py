import numpy as np
import cupy as cp
import random
import pygame
from operator import attrgetter
import Car
import Setting as S


# Function to create the initial population of agents
# start_position: tuple start position
# start_direction: tuple start direction
# amount_of_agents: int amount of agents to create
# sensory_lines: int amount of sensory lines
def initial_population(start_position, start_direction, amount_of_agents = 100, sensory_lines = 32):
    agents = []
    for i in range(amount_of_agents):
        agents.append(Car.Car(start_position, sensory_lines, start_direction))
    return agents


def procreation(agents, amount_of_children = S.amount_of_agents):
    # Sort the agents by fitness
    agents = sorted(agents, key=attrgetter('fitness'), reverse=True)
    # Get the top 10% of the agents
    agents = agents[:int(len(agents) * S.copy_percentage)]
    # Create the children 
    children = []
    # Creating the copys of the best performing agents in that generation
    for agent in agents:
        child = agent
        child.direction = pygame.math.Vector2(S.start_direction)
        child.position = S.start_position
        child.fitness = 0
        children.append(child)

    # creating the children that are the offspring of the best agents.
    for i in range(int(amount_of_children * S.offspring_percentage)):
        # Select two random parents
        parent1 = random.choice(agents)
        parent2 = random.choice(agents)
        # Create a child
        child = Car.Car(parent1.spawn, S.laser_lines, S.start_direction)
        # Crossover
        for i in range(len(child.brain.layers)):
            for j in range(len(child.brain.layers[i].weights)):
                for k in range(len(child.brain.layers[i].weights[j])):
                    if random.random() > 0.5:
                        child.brain.layers[i].weights[j][k] = parent1.brain.layers[i].weights[j][k]
                    else:
                        child.brain.layers[i].weights[j][k] = parent2.brain.layers[i].weights[j][k]
        # Mutation
        if random.random() < S.mutation_chance:
            for i in range(len(child.brain.layers)):
                for j in range(len(child.brain.layers[i].weights)):
                    for k in range(len(child.brain.layers[i].weights[j])):
                        child.brain.layers[i].weights[j][k] += random.uniform(-0.1, 0.1)
        children.append(child)

    # Creating the children that are random
    for i in range(int(amount_of_children * S.random_percentage)):
        children.append(Car.Car(S.start_position, S.laser_lines, S.start_direction))


    return children

