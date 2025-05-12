import numpy as np
import cupy as cp
import random,json, pygame
from operator import attrgetter
import Car
import Setting as S


# Function to create the initial population of agents
# start_position: tuple start position
# start_direction: tuple start direction
# amount_of_agents: int amount of agents to create
# sensory_lines: int amount of sensory lines
def initial_population(map, start_position, start_direction, Genes = None):
    agents = []
    # If there is a genepool to intialize the population with
    if Genes:
        for i, gene in enumerate(Genes):
            # Creating a instance of a car
            agent = Car.Car(start_position, S.laser_lines, start_direction, map.checkpoints.copy())
            # Changing the brain of the agent to the Genes values
            for i in range(len(agent.brain.layers)):
                # Inheriting the Layer Weights
                for j in range(len(agent.brain.layers[i].weights)):
                    for k in range(len(agent.brain.layers[i].weights[j])):
                        agent.brain.layers[i].weights = cp.array(gene[i][0]['weights'].copy())
                # Inheriting the Layer Biases
                for j in range(len(agent.brain.layers[i].biases)):
                    for k in range(len(agent.brain.layers[i].biases[j])):
                        agent.brain.layers[i].biases = cp.array(gene[i][0]['biases'].copy())
            
            agents.append(agent)
        return agents

    # Create random agents based on no genes.
    else:
        for i in range(S.amount_of_agents):
            agents.append(Car.Car(start_position, S.laser_lines, start_direction, map.checkpoints.copy()))
        return agents
    


def procreation(agents, map, start_position, start_direction, amount_of_children = S.amount_of_agents):
    # Sort the agents by fitness
    agents = sorted(agents, key=attrgetter('fitness'), reverse=True)

    # Get the top % of the agents
    agents = agents[:int(len(agents) * S.COPY_PERCENTAGE)]

    # Create the children 
    children = []

    # Creating the copys of the best performing agents in that generation
    for agent in agents:
        child = Car.Car(start_position, S.laser_lines, start_direction, map.checkpoints.copy())
        child.brain = agent.brain
        children.append(child)

    # creating the children that are the offspring of the best agents.
    for i in range(int(amount_of_children * S.OFFSPRING_PERCENTAGE)):
        # Select two random parents
        parent1 = random.choice(agents)
        parent2 = random.choice(agents)
        # Create a child
        child = Car.Car(start_position, S.laser_lines, start_direction, map.checkpoints.copy())
        # Crossover
        for i in range(len(child.brain.layers)):
            # Inheriting the Layer Weights
            for j in range(len(child.brain.layers[i].weights)):
                for k in range(len(child.brain.layers[i].weights[j])):
                    # Parent 1 gene inheretance
                    if random.random() > 0.5:
                        # Random mutation happens
                        if random.random() < S.mutation_chance:
                            child.brain.layers[i].weights[j][k] = parent1.brain.layers[i].weights[j][k].copy() + random.uniform(-S.mutation_size, S.mutation_size)
                        # No mutation happens
                        else:
                            child.brain.layers[i].weights[j][k] = parent1.brain.layers[i].weights[j][k].copy()
                    # Parent 2 gene inheretance
                    else:
                        # Random mutation happens
                        if random.random() < S.mutation_chance:
                            child.brain.layers[i].weights[j][k] = parent2.brain.layers[i].weights[j][k].copy() + random.uniform(-S.mutation_size, S.mutation_size)
                        # No mutation happens
                        else:
                            child.brain.layers[i].weights[j][k] = parent2.brain.layers[i].weights[j][k].copy()
            
            # Inheriting the Layer Biases
            for j in range(len(child.brain.layers[i].biases)):
                for k in range(len(child.brain.layers[i].biases[j])):
                    # Parent 1 gene inheretance
                    if random.random() > 0.5:
                        # Random mutation happens
                        if random.random() < S.mutation_chance:
                            child.brain.layers[i].biases[j][k] = parent1.brain.layers[i].biases[j][k].copy() + random.uniform(-S.mutation_size, S.mutation_size)
                        # No mutation happens
                        else:
                            child.brain.layers[i].biases[j][k] = parent1.brain.layers[i].biases[j][k].copy()
                    # Parent 2 gene inheretance
                    else:
                        # Random mutation happens
                        if random.random() < S.mutation_chance:
                            child.brain.layers[i].biases[j][k] = parent2.brain.layers[i].biases[j][k].copy() + random.uniform(-S.mutation_size, S.mutation_size)
                        # No mutation happens
                        else:
                            child.brain.layers[i].biases[j][k] = parent2.brain.layers[i].biases[j][k].copy()

        children.append(child)

    # Creating the children that are random
    for i in range(int(amount_of_children * S.RANDOM_PERCENTAGE)):
        children.append(Car.Car(start_position, S.laser_lines, start_direction, map.checkpoints.copy()))


    return children
