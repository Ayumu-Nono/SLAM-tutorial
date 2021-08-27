from handler.drawer import Drawer
from params.picture_params import (
    xlim, ylim, figsize, true_nose_length, true_robot_color,
    true_robot_alpha, true_robot_radius, rectangle_color
)


class Picture:
    def __init__(self, drawer: Drawer) -> None:
        assert isinstance(drawer, Drawer)
        self.__drawer: Drawer = drawer

    def save_latest_version(self, path: str) -> bool:
        self.__drawer.set_figure(figsize=figsize, xlim=xlim, ylim=ylim)
        self.__drawer.draw_rectangles(rectangle_color=rectangle_color)
        self.__drawer.draw_status(
            key="true_status", nose_length=true_nose_length,
            robot_color=true_robot_color, robot_alpha=true_robot_alpha,
            robot_radius=true_robot_radius
        )
        self.__drawer.save_fig(path)
        return True
        
        