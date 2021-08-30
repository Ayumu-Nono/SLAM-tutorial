from .hyper_params import mesh_digit, mesh_xs, mesh_ys, n_particle

# Mesh
mesh_digit, mesh_xs, mesh_ys = mesh_digit, mesh_xs, mesh_ys
passing_rate = 0.8
max_distance = 0.5
position_vs_angle_cost_ratio = 0.05
mesh_vs_status_cost_ratio = 1.0

# Particle
n_particle = n_particle
position_scatter_rate: float = 0.2
angle_scatter_rate: float = 0.1
thre_score: float = 0.97
max_iterate: int = 2