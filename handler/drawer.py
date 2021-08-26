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

    def set_figure(self, figsize: tuple, xlim: tuple, ylim: tuple) -> Tuple[Figure, Axes]:
        fig: Figure = plt.figure(figsize=figsize)
        ax: Axes = fig.add_subplot(111)
        ax.set_aspect("equal")
        plt.rcParams["font.size"] = 14
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
        return fig, ax

    def draw_rectangles(self, ax: Axes) -> Axes:
        rs = [
            PatchRectangle(xy=rec.xy, width=rec.width, height=rec.height)
            for rec in self.__rectangle_controller.get_all()
        ]
        for r in rs:
            ax.add_patch(r)
        return ax
