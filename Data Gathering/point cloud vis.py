import matplotlib.pyplot as plt

def plot_xy_from_xyz(file_path):
    x_coords = []
    y_coords = []

    with open(file_path, "r") as f:
        for line in f:
            x, y = map(float, line.split())
            x_coords.append(x)
            y_coords.append(-y)

    plt.figure(figsize=(8, 8))
    plt.scatter(x_coords, y_coords, s=1, c='blue', label='Points')
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("XY Scatter Plot from XYZ File")
    plt.legend()
    plt.grid(True)
    plt.axis('equal')
    plt.show()

plot_xy_from_xyz("Data Gathering\grid_output_10 copy.csv")
