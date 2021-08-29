from .hyper_params import mesh_digit, mesh_xs, mesh_ys

# Mesh
mesh_digit, mesh_xs, mesh_ys = mesh_digit, mesh_xs, mesh_ys
passing_rate = 0.5
max_distance = 10.0
position_vs_angle_cost_ratio = 0.1
mesh_vs_status_cost_ratio = 0.00

# Particle
n_particle: int = 10
position_scatter_rate: float = 0.2
angle_scatter_rate: float = 0.1
thre_score: float = 0.95
max_iterate: int = 3