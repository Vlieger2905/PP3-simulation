import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import griddata

def plot_3d_surface(data):
    # Unpack the data
    agents_core, agents_cutoff, total_time = zip(*data)

    # Create a grid of unique x and y values
    x_range = np.linspace(min(agents_core), max(agents_core), 50)
    y_range = np.linspace(min(agents_cutoff), max(agents_cutoff), 50)
    X, Y = np.meshgrid(x_range, y_range)

    # Interpolate time values onto the grid
    Z = griddata((agents_core, agents_cutoff), total_time, (X, Y), method='cubic')

    # Plot
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')

    # Surface plot
    surf = ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none')

    # Labels
    ax.set_xlabel("Agents per Core")
    ax.set_ylabel("Agents Multi Cutoff")
    ax.set_zlabel("Total Time")  # Now on the vertical axis
    ax.set_title("3D Surface Plot of Time vs Agents")

    # Color bar
    fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10, label="Total Time")

    plt.show()
