# This is the main file to run
import Simulation
import pygame
import Setting as S

def main(Genes = None):
    pygame.init()
    pygame.display.set_caption('Race car simulation')
    simulation = Simulation.Simulation(Genes)
    simulation.Run()


if __name__ == '__main__':
    main("Save Files\Generation 260 at 13-05_20-26.json")