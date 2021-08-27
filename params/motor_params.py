import numpy as np

# Noise
position_noise_rate = 0.3
angle_noise_rate = 0.1

# Time step
dt = 0.01  # [s]

# Initial status
init_position: np.ndarray = np.array([0.5, 0.5])
init_angle: float = 0.0