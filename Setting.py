# Information:
# one pixel is one centimeter irl

import json
import numpy as np

# window settings
FPS = 60 # Setting the frames per second to a certain amount
WIDTH = 1280
HEIGTH = 720

# Information car
car_width = 0.185 # in m
car_length = 0.361 # in m
car_wheelbase = 0.257 # in m
max_steering_angle = 60 # in degrees

# Information lidar
laser_lines = 64
lidar_min_dist = 20
lidar_max_dist = 1200

# Simulation settings
# Map settings
grid_size = 10
# Amount of agents in the simulation
amount_of_agents = 100
# maximum Amount of cores to be used with multiprocessing
max_cores = 10
# minumum amount of agents per core
agents_per_core = 100
# minimum amount of agents alive to use multiprocessing
agents_multi_cutoff = 300
# Amount of steps the simulation will run
simulation_length =  80
# Starting position normal
x_coord = [37 * grid_size, 113 * grid_size]
y_coord = [200 * grid_size, 236 * grid_size]

# Starting direction
start_direction = [(1, 0), (0,1)]

# Hidden layers
hidden_layers = 128, 64, 32  # Example of increasing the size and adding an extra layer

# Amount of agents procreated in the following precentages
COPY_PERCENTAGE = 0.1
OFFSPRING_PERCENTAGE = 0.9
RANDOM_PERCENTAGE = 0
SAVE_PERCENTAGE = 0.1
# Change for mutation to occur
mutation_chance = 0.2
mutation_size = 0.1
# Rewards for the agents
STAYIN_ALIVE_REWARD = 1
CHECKPOINT_REWARD = 300

# Map file
map_file = "Data Gathering\grid_output_10.csv"
checkpoints = [((97, 191), (97, 207)), 
               ((105, 205), (118, 205)), 
               ((105, 254), (118, 254)), 
               ((117, 257), (117, 279)), 
               ((122, 257), (122, 279)),
               ((142, 257), (142, 279)),
               ((162, 257), (162, 279)),
               ((188, 262), (188, 282)), 
               ((231, 276), (225, 255))]
dead_points = [((88* grid_size, 181* grid_size), (128* grid_size, 207* grid_size)),
               ((125* grid_size, 281* grid_size), (102* grid_size, 260* grid_size))
               ]

class NumpyArrayEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)