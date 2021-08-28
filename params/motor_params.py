import numpy as np

from .hyper_params import dt

# Noise
position_noise_rate = 0.3
angle_noise_rate = 0.8

dt = dt

# Initial status
init_position: np.ndarray = np.array([0.5, 0.5])
init_angle: float = 0.0
