import pandas
import json
import numpy


map_file = "Data Gathering\Mapdata\Map of DB.csv"
grid = pandas.read_csv(map_file)
grid = grid.to_numpy()


output_file = "Maps/Map of DB.json"

data = {
    "starting position": [39, 200],
    "starting direction": [1, 0],
    "checkpoints": [[
            [
                97,
                191
            ],
            [
                97,
                207
            ]
        ],
        [
            [
                105,
                205
            ],
            [
                118,
                205
            ]
        ],
        [
            [
                105,
                254
            ],
            [
                118,
                254
            ]
        ],
        [
            [
                117,
                257
            ],
            [
                117,
                279
            ]
        ],
        [
            [
                122,
                257
            ],
            [
                122,
                279
            ]
        ],
        [
            [
                142,
                257
            ],
            [
                142,
                279
            ]
        ],
        [
            [
                162,
                257
            ],
            [
                162,
                279
            ]
        ],
        [
            [
                188,
                262
            ],
            [
                188,
                282
            ]
        ],
        [
            [
                231,
                276
            ],
            [
                225,
                255
            ]
        ]],
    "grid": grid.tolist()
}

with open(output_file, "w") as json_file:
    json.dump(data, json_file, indent=4)



