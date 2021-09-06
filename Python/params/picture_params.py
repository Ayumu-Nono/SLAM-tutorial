from params.hyper_params import mesh_digit, mesh_xs, mesh_ys, n_particle


xlim: tuple = (-0.1, 10.1)
ylim: tuple = (-0.1, 10.1)
figsize: tuple = (12, 10)

# True robot
true_nose_length: float = 0.3
true_robot_color: str = "black"
true_robot_alpha: float = 1.0
true_robot_radius: float = 0.2

# Pred robot 
pred_nose_length: float = 0.3
pred_robot_color: str = "green"
pred_robot_alpha: float = 1.0
pred_robot_radius: float = 0.2

# Smoothed robot 
smtd_nose_length: float = 0.3
smtd_robot_color: str = "red"
smtd_robot_alpha: float = 1.0
smtd_robot_radius: float = 0.2

# Rectangle
rectangle_color = "gray"

# Scan
scan_mesh_alpha: float = 0.3
scan_mesh_zorder: int = 10

true_scan_color: str = "black"
true_scan_cmap: str = "binary"
true_scan_vrange: tuple = (0.0, 1.0)

pred_scan_color: str = "green"
pred_scan_cmap: str = "greens"
pred_scan_vrange: tuple = (0., 2.)

smtd_scan_color: str = "red"
smtd_scan_cmap: str = "bwr"
smtd_scan_vrange: tuple = (-1., 1.)


# True orbit
true_orbit_color: str = "black"
# Pred orbit
pred_orbit_color: str = "green"
# Smtd orbit
smtd_orbit_color: str = "red"


# Mesh
mesh_digit, mesh_xs, mesh_ys = mesh_digit, mesh_xs, mesh_ys

# Particle
n_particle = n_particle