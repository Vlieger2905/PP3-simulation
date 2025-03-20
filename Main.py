# This is the main file to run
import Simulation
import pygame

# simulation = Simulation.Simulation()

# simulation.Run()
def main(amount_of_agents, cores):
    pygame.init()
    pygame.display.set_caption('Race car simulation')
    simulation = Simulation.Simulation(amount_of_agents)
    simulation.Run(cores)

# Amount of agents in teh simulation
amount_of_agents = 200
# Amount of cores to be used with multiprocessing
cores = 10
if __name__ == '__main__':
    main(amount_of_agents, cores)
    