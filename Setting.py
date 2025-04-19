# Information:
# one pixel is one centimeter irl

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
laser_lines = 32
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
simulation_length =  300
# Starting position
start_position = (200*grid_size, 37*grid_size)
# Starting direction
start_direction = (1, 0)
# Amount of agents procreated in the following precentages
copy_percentage = 0.1
offspring_percentage = 0.8
random_percentage = 0.1
# Change for mutation to occur
mutation_chance = 0.1


