from typing import Tuple

from handler.drawer import Drawer
from params.picture_params import xlim, ylim, figsize


class Picture:
    def __init__(self, drawer: Drawer) -> None:
        assert isinstance(drawer, Drawer)
        self.__drawer: Drawer = drawer

    def save_latest_version(self, path: str) -> bool:
        self.__drawer.set_figure(figsize=figsize, xlim=xlim, ylim=ylim)
        self.__drawer.draw_rectangles()
        self.__drawer.save_fig(path)
        return True
        
        