import numpy as np

dt: float = 0.01  # [s]

# Mesh scan
mesh_digit: int = 1
mesh_xs: np.ndarray = np.linspace(-0.1, 10.1, 103).round(decimals=mesh_digit)
mesh_ys: np.ndarray = np.linspace(-0.1, 10.1, 103).round(decimals=mesh_digit)

# Particle
n_particle: int = 50000