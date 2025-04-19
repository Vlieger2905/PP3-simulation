import numpy as np
import open3d as o3d
import matplotlib.pyplot as plt

def generate_point_clouds():
    """
    Generates a global point cloud and a local point cloud that is misaligned but partially overlaps.
    """
    # Create a global point cloud (Nx3 for 3D data)
    global_points = np.random.rand(100, 3) * 10  # Points in a 10x10x10 space

    # Create a local point cloud that is slightly translated and rotated
    angle = np.radians(10)  # Rotate by 10 degrees
    rotation_matrix = o3d.geometry.get_rotation_matrix_from_xyz((0, 0, angle))
    translation = np.array([2, 1, 0])  # Shift by (2,1,0)

    # Apply transformation (rotation + translation)
    local_points = (global_points[:50] @ rotation_matrix.T) + translation  # Only take first 50 points

    return global_points, local_points

def align_and_merge(global_points, local_points):
    """
    Aligns the local points to the global map using ICP and merges them.
    """
    # Convert numpy arrays to Open3D point clouds
    global_pcd = o3d.geometry.PointCloud()
    global_pcd.points = o3d.utility.Vector3dVector(global_points)

    local_pcd = o3d.geometry.PointCloud()
    local_pcd.points = o3d.utility.Vector3dVector(local_points)

    # Perform ICP registration
    threshold = 0.5  # Distance threshold for point matching
    icp_result = o3d.pipelines.registration.registration_icp(
        local_pcd, global_pcd, threshold, np.eye(4),
        o3d.pipelines.registration.TransformationEstimationPointToPoint()
    )

    # Apply the transformation to the local points
    local_pcd.transform(icp_result.transformation)
    transformed_local = np.asarray(local_pcd.points)

    # Merge the transformed local points with the global map
    updated_global_map = np.vstack([global_points, transformed_local])

    return transformed_local, updated_global_map

# Generate test point clouds
global_points, local_points = generate_point_clouds()

# Align and merge
transformed_local, updated_global_map = align_and_merge(global_points, local_points)

# Visualization
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(global_points[:, 0], global_points[:, 1], global_points[:, 2], c='blue', label="Global Map (Original)")
ax.scatter(local_points[:, 0], local_points[:, 1], local_points[:, 2], c='red', label="Local Map (Before Alignment)")
ax.scatter(transformed_local[:, 0], transformed_local[:, 1], transformed_local[:, 2], c='green', label="Local Map (After Alignment)")
ax.legend()
ax.set_title("ICP Alignment of Partially Overlapping Point Clouds")
plt.show()
