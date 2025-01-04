# import numpy as np
# import cupy as cp
# import time

# # Set the matrix size
# N = 1000

# # Timing numpy matrix multiplication
# start_time = time.time()
# # Create random matrices using numpy and cupy
# A_np = np.random.rand(N, N)
# B_np = np.random.rand(N, N)
# C_np = np.dot(A_np, B_np)
# numpy_time = time.time() - start_time

# # # Timing cupy matrix multiplication (on GPU)
# # start_time = time.time()
# # A_cp = cp.random.rand(N, N)
# # B_cp = cp.random.rand(N, N)
# # C_cp = cp.dot(A_cp, B_cp)
# # cupy_time = time.time() - start_time

# # Print the results
# print(f"Time taken for numpy matrix multiplication: {numpy_time:.6f} seconds")
# # print(f"Time taken for cupy matrix multiplication: {cupy_time:.6f} seconds")