import pygame, random, os, json
import sys
import time, datetime
from operator import attrgetter
import Car, Map
import multiprocessing_test as mt
import populator as pop
import Setting as S


class Simulation:
    def __init__(self, Genes = None):
        #Setting up the game class 
        self.screen = pygame.display.set_mode((S.WIDTH, S.HEIGTH))
        # Setting up the fps control system of the game
        self.clock =  pygame.time.Clock()
        # Map to train the cars on
        self.map = Map.Map(S.map_file)
        # Picking starting location and direction
        self.index = 0
        self.start_position = (self.map.start_pos[0] * S.grid_size, self.map.start_pos[1] * S.grid_size)
        self.start_direction = self.map.start_direction
        self.old_offset = (0,0)
        # Items for the management of the population
        self.agent_sensory_lines = S.laser_lines
        if Genes:   
            Genes = self.Load(Genes)
            self.agents = pop.initial_population(self.map,self.start_position,self.start_direction, Genes)

        else:
            self.agents = pop.initial_population(self.map,self.start_position,self.start_direction)
            self.generation = 1
            
            # Lists to track the growth of the agents.
            self.top_fitness = []
            self.average_fitness = []

        self.died_agents = []
        

    def Run(self):
        steps = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        list_to_save = self.agents.copy()
                        list_to_save.extend(self.died_agents.copy())
                        self.Save(list_to_save)
            # Drawing the screen and updating it
            self.screen.fill("white")
            
            # Creating the lidar lines for each agent
            for id, agent in enumerate(self.agents):
                agent.lidar = mt.create_lines(agent.position, agent.direction,self.agent_sensory_lines)

            # Get a list of distances and directions for each agent.
            info = [(id, agent.position,agent.lidar, self.map.rects) for  id, agent in enumerate(self.agents)]
            if self.agents.__len__() > S.agents_multi_cutoff and self.agents.__len__() > S.agents_per_core :
                cores = min(self.agents.__len__() // S.agents_per_core, S.max_cores)
                results = mt.multiprocess_lines(info, cores)

            # Getting the distances of the agents without multithreading.
            elif self.agents.__len__() <= S.agents_multi_cutoff or self.agents.__len__() <= S.agents_per_core:
                results = [mt.collide_lines(*args) for args in info]

            # Index 0 = id, Index 1 = End position lidar lines, Index 2 = Distance to obstacle
            for i, item in enumerate(results):
                # Setting the lidar endpoints
                self.agents[i].lidar_endpoints =item[1]
                # Setting the distance to the obstacle
                self.agents[i].lidar = item[2]

            # Updating the agents
            self.update_agents()

            # Drawing the map, agents, died agents, checkpoints. 
            self.draw(self.screen)

            # Render text
            font = pygame.font.Font(None, 36)  # Use default font with size 36
            text = font.render(f"Generation: {self.generation}", True, (0, 0, 0))  # Black color
            text_rect = text.get_rect(center=(S.WIDTH // 2, 30))  # Position at the top center
            self.screen.blit(text, text_rect)

            # updating the screen
            pygame.display.update()
            steps += 1
            self.clock.tick()

            # If the simulation has run for the amount of steps or all agents are dead a new population gets made
            if steps >= S.simulation_length or self.agents.__len__() == 0:
                # Adding all the died agents to the agents list
                self.agents.extend(self.died_agents)
                
                agents = sorted(self.agents, key=attrgetter('fitness'), reverse=True)
                self.top_fitness.append(agents[0].fitness)
                self.average_fitness.append(sum(agent.fitness for agent in agents[:10]) / 10)

                # Saving the neural network information every 10 generations. 
                if self.generation % S.save_file_per_gen == 0:
                    self.Save(self.agents)

                # Creating a new population based on the previous population
                # Picking starting location and direction
                self.start_position = (int((self.map.start_pos[0] + random.uniform(-3,3)) * S.grid_size) , int((self.map.start_pos[1] + random.uniform(-3,3))*S.grid_size)) 
                self.start_direction = (
                    self.map.start_direction[0] + random.uniform(-0.3, 0.3),
                    self.map.start_direction[1] + random.uniform(-0.3, 0.3)
                )
                # Creating new population
                self.agents = pop.procreation(self.agents,self.map,self.start_position,self.start_direction)
                # Resetting the died agents and the steps
                self.died_agents = []
                steps = 0
                self.generation += 1          
            
            
    
    def update_agents(self):
        # List to store all the agents that need to be removed to prevent runtime errors
        agents_to_remove = []

        # Updating each agent
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
            # update the hitbox/outline of the car
            agent.update_car_outline()
            
            
            # Give the agent a reward
            self.give_reward(agent)

            # Check if the car hits the dead boundary to force the agents to go to the right.
            collided = False
            for boundary in S.dead_points:
                for line in agent.outline:
                    collided = self.map.lines_collide(line, boundary)
                    if collided:
                        break
                if collided:
                    break

            if collided == False:
                # Check if the agent collides with the walls
                collided = agent.check_collision(self.map.rects)

            if collided:
                self.died_agents.append(agent)
                agents_to_remove.append(agent)
        
        # Removing the agents from the self.agents
        for agent in agents_to_remove:
            self.agents.remove(agent)
                
    # Function to give the agents rewards
    # Surviving one step gives a reward of 1
    # Hitting a checkpoint gives out rewards
    #TODO More rewards should be added later.
    def give_reward(self,agent):
    # If the agent is still alive reward one point.
        agent.fitness += S.STAYIN_ALIVE_REWARD

        # Check whether agents hit a checkpoint.
        for agent in self.agents:
            # For each checkpoint
            hit = False
            for i, checkpoint in enumerate(agent.checkpoints):
                # Check whether any of the lines of the agent intersect with a checkpoint
                for line in agent.outline:
                    # If the agent collides with the checkpoint give it rewards and remove the checkpoint.
                    if self.map.lines_collide(checkpoint, line):
                        agent.fitness += S.CHECKPOINT_REWARD
                        hit = True
                        agent.checkpoints.remove(checkpoint)
                        break
            if hit:
                break

    def draw(self, surface):
        # Find the agent with the highest fitness
        if self.agents:
            best_agent = max(self.agents, key=lambda agent: agent.fitness)
            # Center the screen on the best agent
            offset_x = S.WIDTH // 2 - best_agent.position[0]
            offset_y = S.HEIGTH // 2 - best_agent.position[1]
            self.old_offset = (offset_x, offset_y)

            # Draw all agents with the offset
            for agent in self.agents:
                agent.draw(surface, offset=(offset_x, offset_y))
            
            # Drawing the agents that are dead
            for agent in self.died_agents:
                agent.draw(self.screen, offset=(offset_x, offset_y))

            # Highlight the best agent
            best_agent.best_draw(surface, (offset_x, offset_y), (0, 255, 0))
            self.map.draw(surface, offset=(offset_x, offset_y))

            for line in S.dead_points:
                pygame.draw.line(surface, (255, 0, 0), 
                                 (int(line[0][0] + offset_x), int(line[0][1] + offset_y)), 
                                 (int(line[1][0] + offset_x), int(line[1][1] + offset_y)), 2)
        else:
            # If no agents are alive, just draw the map
            self.map.draw(surface, self.old_offset)
            # Drawing the agents that are dead
            for agent in self.died_agents:
                agent.draw(self.screen, self.old_offset)
        
    # Function to save the best performing agents.
    def Save(self, agents):
        genePool = []
        for agent in agents:
            genePool.append(agent.brain.SavingSperm())
        
# Making a library to store the data in for export.
        data = {
            'generation': self.generation,
            'top fitness': self.top_fitness,
            'average fitness': self.average_fitness,
            'Genes': genePool,
        }

# Creating filename
        # Where the information is saved
        save_folder = "Save Files"
        file_name = f"Generation {self.generation} at {datetime.datetime.now().strftime("%d-%m_%H-%M")}"

        # Ensure the save folder exists
        os.makedirs(save_folder, exist_ok=True)
        fileName = os.path.join(save_folder, file_name + ".json")
        with open(fileName, 'w') as file: 
            json.dump(data, file, indent=4, cls=S.NumpyArrayEncoder)

    # Function to load the saved data
    def Load(self, file_path):
        # Reading info from the json file
        with open(file_path, 'r') as file:
            data = json.load(file)

        # Setting the self.generation from the safe file
        self.generation = data['generation']
        # List that can be used to show growth.
        self.top_fitness = data['top fitness']
        self.average_fitness = data['average fitness']

        loaded_genes = data['Genes']

        return loaded_genes