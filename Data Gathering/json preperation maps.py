import pandas
import json
import numpy


map_file = "Data Gathering\Mapdata\Test Straight.csv"
grid = pandas.read_csv(map_file)
grid = grid.to_numpy()


output_file = "Maps/Test map straigth.json"

data = {
    "starting position": [3, 3],
    "starting direction": [1, 0],
    "checkpoints" : [[[100,1],[100,14]]],
    "grid": grid.tolist()
}

with open(output_file, "w") as json_file:
    json.dump(data, json_file, indent=4)



