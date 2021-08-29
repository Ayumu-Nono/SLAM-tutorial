import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle as PatchRectangle
from matplotlib.patches import Circle
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize

from db.controller.rectangle_controller import RectangleController
from db.controller.status_controller import StatusController
from db.controller.scan_controller import ScanController


class Drawer:
    def __init__(
        self,
        rectangle_controller: RectangleController,
        true_status_controller: StatusController,
        pred_status_controller: StatusController,
        smtd_status_controller: StatusController,
        scan_controller: ScanController
    ) -> None:
        assert isinstance(rectangle_controller, RectangleController)
        assert isinstance(true_status_controller, StatusController)
        assert isinstance(pred_status_controller, StatusController)
        assert isinstance(smtd_status_controller, StatusController)
        assert isinstance(scan_controller, ScanController)
        self.__rectangle_controller = rectangle_controller
        self.__true_status_controller = true_status_controller
        self.__pred_status_controller = pred_status_controller
        self.__smtd_status_controller = smtd_status_controller
        self.__scan_controller = scan_controller
        self.__fig: Figure = None
        self.__ax: Axes = None

    def set_figure(self, figsize: tuple, xlim: tuple, ylim: tuple) -> bool:
        self.__fig = plt.figure(figsize=figsize)
        self.__ax = self.__fig.add_subplot(111)
        self.__ax.set_aspect("equal")
        plt.rcParams["font.size"] = 14
        self.__ax.set_xlim(xlim)
        self.__ax.set_ylim(ylim)
        return True

    def draw_rectangles(self, rectangle_color: str) -> bool:
        rs = [
            PatchRectangle(
                xy=rc[0], width=rc[1],
                height=rc[2], fc=rectangle_color
            )
            for rc in self.__rectangle_controller.get_all_as_keystyle()
        ]
        for r in rs:
            self.__ax.add_patch(r)
        return True

    def draw_status(
        self, species: str, nose_length: float, robot_color: str,
        robot_alpha: float, robot_radius: float
    ) -> bool:
        if species == "true_status":
            status_controller = self.__true_status_controller
        elif species == "pred_status":
            status_controller = self.__pred_status_controller
        elif species == "smtd_status":
            status_controller = self.__smtd_status_controller
        else:
            raise KeyError("Unknown key value", species)
        position = status_controller.get_latest_position_as_arr()
        angle = status_controller.get_latest_angle_as_float()
        x, y = position
        x_nose = x + nose_length * np.cos(angle)
        y_nose = y + nose_length * np.sin(angle)
        self.__ax.plot(
            [x, x_nose], [y, y_nose],
            color=robot_color, alpha=robot_alpha
        )
        c = Circle(
            xy=(x, y), radius=robot_radius, fill=False,
            color=robot_color, alpha=robot_alpha
        )
        self.__ax.add_patch(c)
        return True

    def draw_scan(self, species: str, scan_color: str) -> bool:
        if species == "true_scan":
            status_controller = self.__true_status_controller
        elif species == "smtd_scan":
            status_controller = self.__smtd_status_controller
        scan_controller = self.__scan_controller
        position = status_controller.get_latest_position_as_arr()
        angle = status_controller.get_latest_angle_as_float()
        scan_points = scan_controller.get_latest_as_cartesian_arr(
            self_position=position, self_angle=angle
        )
        self.__ax.scatter(
            scan_points[:, 0], scan_points[:, 1],
            fc="white", ec=scan_color, zorder=10
        )
        return True
    
    def draw_scan_mesh(
        self, species: str, scan_color: str,
        mesh_digit: int, mesh_xs: np.ndarray, mesh_ys: np.ndarray,
        cmap: str, vmin: float, vmax: float, zorder: int, alpha: float
    ) -> bool:
        if species == "true_scan":
            status_controller = self.__true_status_controller
        elif species == "pred_scan":
            status_controller = self.__pred_status_controller
        elif species == "smtd_scan":
            status_controller = self.__smtd_status_controller
        scan_controller = self.__scan_controller
        position = status_controller.get_latest_position_as_arr()
        angle = status_controller.get_latest_angle_as_float()
        scan_mesh: np.ndarray = scan_controller.get_latest_as_mesh(
            self_position=position, self_angle=angle,
            mesh_digit=mesh_digit, mesh_xs=mesh_xs, mesh_ys=mesh_ys
        )
        X, Y = np.meshgrid(mesh_xs, mesh_ys)
        self.__ax.pcolormesh(
            X, Y, scan_mesh.T, shading="auto", norm=Normalize(vmin, vmax),
            cmap=cmap, zorder=zorder, alpha=alpha
        )
        return True

    def draw_orbit(self, species: str, orbit_color: str) -> bool:
        if species == "true_orbit":
            status_controller = self.__true_status_controller
        elif species == "smtd_orbit":
            status_controller = self.__smtd_status_controller
        elif species == "pred_orbit":
            status_controller = self.__smtd_status_controller
        else:
            raise KeyError("Unknown species", species)
        positions = status_controller.get_all_position_as_arr()
        self.__ax.plot(positions[:, 0], positions[:, 1], color=orbit_color, label=species)
        return True

    def add_legend(self) -> bool:
        self.__ax.legend()
        return True

    def save_fig(self, path: str) -> bool:
        self.__fig.savefig(path)
        plt.close()
        return True

