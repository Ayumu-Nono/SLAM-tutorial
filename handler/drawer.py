import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle as PatchRectangle
from matplotlib.patches import Circle
import matplotlib.pyplot as plt

from db.controller.rectangle_controller import RectangleController
from db.controller.status_controller import StatusController


class Drawer:
    def __init__(
        self,
        rectangle_controller: RectangleController,
        true_status_controller: StatusController
    ) -> None:
        assert isinstance(rectangle_controller, RectangleController)
        assert isinstance(true_status_controller, StatusController)
        self.__rectangle_controller = rectangle_controller
        self.__true_status_controller = true_status_controller
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
                xy=rec.xy, width=rec.width,
                height=rec.height, fc=rectangle_color
            )
            for rec in self.__rectangle_controller.get_all()
        ]
        for r in rs:
            self.__ax.add_patch(r)
        return True

    def draw_status(
        self, key: str, nose_length: float, robot_color: str,
        robot_alpha: float, robot_radius: float
    ) -> bool:
        if key == "true_status":
            status_controller = self.__true_status_controller
        else:
            raise KeyError("Unknown key value", key)
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


    def save_fig(self, path: str) -> bool:
        self.__fig.savefig(path)
        plt.close()
        return True

