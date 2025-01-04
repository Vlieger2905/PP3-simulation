# This is the main file to run
import Simulation
import pygame

# simulation = Simulation.Simulation()

# simulation.Run()
def main():
    pygame.init()
    pygame.display.set_caption('Race car simulation')
    simulation = Simulation.Simulation()
    simulation.Run()

if __name__ == '__main__':
    main()
    