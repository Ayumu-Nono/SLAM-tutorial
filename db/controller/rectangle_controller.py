from typing import List

import numpy as np

from model.rectangle import Rectangle
from db.interactor.rectangle_interactor import RectangleInteractor


class RectangleController:
    def __init__(self) -> None:
        self.__rectangle_interactor: RectangleInteractor = RectangleInteractor()

    def push_with_arr(self, ps: np.ndarray) -> bool:
        assert isinstance(ps, np.ndarray)
        assert ps.shape == (4, 2)
        i_lefts = np.argmin(ps[:, 0])
        i_rights = np.argmax(ps[:, 0])
        i_belows = np.argmin(ps[:, 1])
        i_uppers = np.argmax(ps[:, 1])
        i_upper_left = np.intersect1d(i_lefts, i_uppers)[0]
        i_upper_right = np.intersect1d(i_rights, i_uppers)[0]
        i_below_left = np.intersect1d(i_lefts, i_belows)[0]
        # i_below_right = np.intersect1d(i_rights, i_belows)[0]
        x0, y0 = ps[i_below_left]
        width = np.abs(ps[i_upper_right] - ps[i_upper_left])
        height = np.abs(ps[i_upper_left] - ps[i_below_left])
        rectangle = Rectangle(xy=(x0, y0), width=width, height=height)
        is_success: bool = self.__rectangle_interactor.push(rectangle)
        return is_success
    
    def push_with_keys(self, xy: tuple, width: float, height: float) -> bool:
        rectangle: Rectangle = Rectangle(xy, width, height)
        is_success: bool = self.__rectangle_interactor.push(rectangle)
        return is_success

    def get_all(self) -> List[Rectangle]:
        return self.__rectangle_interactor.get_all()
