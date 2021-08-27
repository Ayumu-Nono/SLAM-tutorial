from typing import List

import numpy as np
from numpy.lib.arraysetops import isin

from model.rectangle import Rectangle
from db.interactor.rectangle_interactor import RectangleInteractor


class RectangleController:
    def __init__(self) -> None:
        self.__rectangle_interactor: RectangleInteractor = RectangleInteractor()

    def push_with_arr(self, ps: np.ndarray) -> bool:
        assert isinstance(ps, np.ndarray)
        assert ps.shape == (4, 2)
        xmin = np.min(ps[:, 0])
        xmax = np.max(ps[:, 0])
        ymin = np.min(ps[:, 1])
        ymax = np.max(ps[:, 1])
        assert xmin < xmax
        assert ymin < ymax
        x0, y0 = xmin, ymin
        dx = float(xmax - xmin)
        dy = float(ymax - ymin)
        rectangle = Rectangle(xy=(x0, y0), width=dx, height=dy)
        is_success: bool = self.__rectangle_interactor.push(rectangle)
        return is_success
    
    def push_with_keys(self, xy: tuple, width: float, height: float) -> bool:
        rectangle: Rectangle = Rectangle(xy, width, height)
        is_success: bool = self.__rectangle_interactor.push(rectangle)
        return is_success

    def get_all(self) -> List[Rectangle]:
        return self.__rectangle_interactor.get_all()
