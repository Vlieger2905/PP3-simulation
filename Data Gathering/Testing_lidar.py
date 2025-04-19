from rplidar import RPLidar
import matplotlib.pyplot as plt
import numpy as np

PORT_NAME = 'COM5'  # Or COMx on Windows, e.g., 'COM3'

lidar = RPLidar(PORT_NAME)

def update_plot(scan):
    plt.cla()
    angles = np.array([measurement[1] for measurement in scan])
    distances = np.array([measurement[2] for measurement in scan])
    
    xs = distances * np.cos(np.radians(angles))
    ys = distances * np.sin(np.radians(angles))

    plt.plot(xs, ys, '.')
    plt.xlim(-6000, 6000)
    plt.ylim(-6000, 6000)
    plt.title('RPLiDAR A1M8 Live Scan')
    plt.pause(0.001)

try:
    print('Press Ctrl+C to stop...')
    plt.figure()
    for scan in lidar.iter_scans():
        update_plot(scan)

except KeyboardInterrupt:
    print('Stopping...')

finally:
    lidar.stop()
    lidar.disconnect()
