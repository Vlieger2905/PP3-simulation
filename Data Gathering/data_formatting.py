import numpy as np
import math
import os

# Read the scan data
path_input_folder = "Data Gathering\Data gathering\Measurement data"
path_ouput_folder = "Data Gathering\Data gathering\Converted Data"
files = os.listdir(path_input_folder)

# Sort files numerically based on the number in the filename
files = sorted(files, key=lambda x: int(''.join(filter(str.isdigit, x))))

input_files = []
output_files = []

for i, file in enumerate(files):
    file = os.path.join(path_input_folder, file)
    input_files.append(file)
    output_files.append(os.path.join(path_ouput_folder, f"output_{i}.xyz"))

for i in range(len(input_files)):
    # Open the output file for writing
    with open(input_files[i], "r") as f, open(output_files[i], "w") as out:
        for line in f:
            if line.startswith("#") or not line.strip():
                continue  # Skip header and empty lines
            
            angle, distance, _ = map(float, line.split())  # Extract values
            angle_rad = math.radians(angle)  # Convert degrees to radians

            # Convert to Cartesian coordinates
            x = distance * np.cos(angle_rad)
            y = distance * np.sin(angle_rad)
            z = 0

            # Write to .xyz file
            out.write(f"{x:.3f} {y:.3f} {z:.3f}\n")

print(f"Converted data saved to {path_ouput_folder}")
