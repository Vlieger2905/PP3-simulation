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
    main("Save Files\Generation 564 Agents able to turn on unlimeted map.json")