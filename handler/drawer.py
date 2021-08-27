from typing import Tuple

from matplotlib.axes import Axes
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle as PatchRectangle

from db.controller.rectangle_controller import RectangleController


class Drawer:
    def __init__(
        self,
        rectangle_controller: RectangleController
    ) -> None:
        self.__rectangle_controller = rectangle_controller
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

    def draw_rectangles(self) -> bool:
        rs = [
            PatchRectangle(xy=rec.xy, width=rec.width, height=rec.height)
            for rec in self.__rectangle_controller.get_all()
        ]
        for r in rs:
            self.__ax.add_patch(r)
        return True

    def save_fig(self, path: str) -> bool:
        self.__fig.savefig(path)
        return True

