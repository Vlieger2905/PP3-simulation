import pandas
import json
import numpy


map_file = "Data Gathering\Mapdata\grid_output_10 limited boundaries.csv"
grid = pandas.read_csv(map_file)
grid = grid.to_numpy()


output_file = "Maps/Test map limited bound DB .json"

data = {
    "starting position": [39, 200],
    "starting direction": [1, 0],
    "checkpoints": [],
    "grid": grid.tolist()
}

with open(output_file, "w") as json_file:
    json.dump(data, json_file, indent=4)



