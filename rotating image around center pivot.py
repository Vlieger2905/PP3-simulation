import numpy as np
import matplotlib.pyplot as plt
import math

# Inputs
center = (0, 0)  # Center position (cx, cy)
length = 1200       # Length of each line
direction = (1, 1)  # Initial direction vector (dx, dy)

# Normalize the direction vector
magnitude = np.sqrt(direction[0]**2 + direction[1]**2)
unit_vector = (direction[0] / magnitude, direction[1] / magnitude)

# Prepare the plot
plt.figure(figsize=(8, 8))
plt.xlim(-length - 1, length + 1)
plt.ylim(-length - 1, length + 1)
plt.gca().set_aspect('equal', adjustable='box')
amount = 4
# Generate and draw lines
for i in range(amount):
    angle = i * (2*math.pi / amount)
    # Rotate the direction vector
    dx_rot = np.cos(angle) * unit_vector[0] - np.sin(angle) * unit_vector[1]
    dy_rot = np.sin(angle) * unit_vector[0] + np.cos(angle) * unit_vector[1]
    # Scale to length and calculate endpoint
    endpoint = (center[0] + length * dx_rot, center[1] + length * dy_rot)
    # Draw line
    plt.plot([center[0], endpoint[0]], [center[1], endpoint[1]], color='blue', lw=0.5)

# Show the plot
plt.show()
