# This is the main file to run
import Simulation
import pygame
import Setting as S

def main(amount_of_agents, max_cores, simulation_length, agents_core, agents_cutoff):
    pygame.init()
    pygame.display.set_caption('Race car simulation')
    simulation = Simulation.Simulation(amount_of_agents, S.start_position, S.start_direction)
    simulation.Run(max_cores, agents_core, agents_cutoff, simulation_length)


if __name__ == '__main__':
    main(S.amount_of_agents, S.max_cores, S.simulation_length, S.agents_per_core, S.agents_multi_cutoff)
    