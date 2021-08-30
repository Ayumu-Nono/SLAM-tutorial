from handler.drawer import Drawer
from params.picture_params import (
    xlim, ylim, figsize, true_nose_length, true_robot_color,
    true_robot_alpha, true_robot_radius, rectangle_color, true_scan_color,
    true_orbit_color, smtd_nose_length, smtd_robot_alpha, smtd_orbit_color,
    smtd_robot_radius, smtd_robot_color, smtd_scan_color,
    pred_nose_length, pred_orbit_color, pred_robot_alpha, pred_robot_color,
    pred_robot_radius, pred_scan_cmap, pred_scan_color, pred_scan_vrange,
    mesh_digit, mesh_xs, mesh_ys,
    true_scan_cmap, true_scan_vrange, smtd_scan_cmap, smtd_scan_vrange,
    scan_mesh_alpha, scan_mesh_zorder, n_particle
)


class Picture:
    def __init__(self, drawer: Drawer) -> None:
        assert isinstance(drawer, Drawer)
        self.__drawer: Drawer = drawer

    def save_latest_version(self, path: str) -> bool:
        self.__drawer.set_figure(figsize=figsize, xlim=xlim, ylim=ylim)
        self.__drawer.draw_rectangles(rectangle_color=rectangle_color)
        self.__drawer.draw_status(
            species="true_status", nose_length=true_nose_length,
            robot_color=true_robot_color, robot_alpha=true_robot_alpha,
            robot_radius=true_robot_radius
        )
        self.__drawer.draw_status(
            species="pred_status", nose_length=pred_nose_length,
            robot_color=pred_robot_color, robot_alpha=pred_robot_alpha,
            robot_radius=pred_robot_radius
        )
        self.__drawer.draw_status(
            species="smtd_status", nose_length=smtd_nose_length,
            robot_color=smtd_robot_color, robot_alpha=smtd_robot_alpha,
            robot_radius=smtd_robot_radius
        )
        # self.__drawer.draw_scan(
        #     species="true_scan", scan_color=true_scan_color
        # )
        # self.__drawer.draw_scan(
        #     species="smtd_scan", scan_color=smtd_scan_color
        # )
        self.__drawer.draw_scan_mesh(
            species="true_scan", scan_color=true_scan_color,
            mesh_digit=mesh_digit, mesh_xs=mesh_xs, mesh_ys=mesh_ys,
            cmap=true_scan_cmap,
            vmin=true_scan_vrange[0], vmax=true_scan_vrange[1],
            zorder=scan_mesh_zorder, alpha=scan_mesh_alpha
        )
        self.__drawer.draw_scan_mesh(
            species="smtd_scan", scan_color=smtd_scan_color,
            mesh_digit=mesh_digit, mesh_xs=mesh_xs, mesh_ys=mesh_ys,
            cmap=smtd_scan_cmap,
            vmin=smtd_scan_vrange[0], vmax=smtd_scan_vrange[1],
            zorder=scan_mesh_zorder, alpha=scan_mesh_alpha
        )
        self.__drawer.draw_orbit(
            species="true_orbit", orbit_color=true_orbit_color
        )
        self.__drawer.draw_orbit(
            species="pred_orbit", orbit_color=pred_orbit_color
        )
        self.__drawer.draw_orbit(
            species="smtd_orbit", orbit_color=smtd_orbit_color
        )
        self.__drawer.add_legend()
        self.__drawer.add_title(n_particle=n_particle)
        self.__drawer.save_fig(path)
        return True
