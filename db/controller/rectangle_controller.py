from typing import List, Tuple

import numpy as np

from model.rectangle import Rectangle
from db.interactor.rectangle_interactor import RectangleInteractor


class RectangleController:
    def __init__(self) -> None:
        self.__rectangle_interactor: RectangleInteractor = RectangleInteractor()

    def push_with_arr(self, ps: np.ndarray) -> int:
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
        assert is_success
        return self.__rectangle_interactor.get_len()

    def push_with_keys(self, xy: tuple, width: float, height: float) -> int:
        rectangle: Rectangle = Rectangle(xy, width, height)
        is_success: bool = self.__rectangle_interactor.push(rectangle)
        assert is_success
        return self.__rectangle_interactor.get_len()

    def get_all_as_keystyle(self) -> List[Tuple[tuple, float, float]]:
        val = [
            (rc.xy, rc.width, rc.height)
            for rc in self.__rectangle_interactor.get_all()
        ]
        return val

    def get_all_segments_as_arr(self) -> np.ndarray:
        """
            (rectangle数, 4辺, ペア, 座標)の4次元 -> (segment数, ペア, 座標)に変換
        """
        val: np.ndarray = np.array([
            rc.segments for rc in self.__rectangle_interactor.get_all()
        ])
        n_edge: int = 4
        n_pair: int = 2
        n_coor: int = 2
        n_rc: int = len(val)
        assert n_rc > 1
        new_val = val.reshape((n_rc * n_edge, n_pair, n_coor))
        assert new_val.size == val.size
        return new_val
        



