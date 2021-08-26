from typing import List
import numpy as np

from db.controller.rectangle_controller import RectangleController


class Creater:
    def __init__(
        self,
        rectangle_controller: RectangleController
    ) -> None:
        self.__rectangle_controller: RectangleController = RectangleController()

    def create_obstacles(self, obstacles: np.ndarray) -> bool:
        """(rectangle数, 点の数, 座標)の3次元"""
        assert obstacles.ndim == 3
        is_success_arr: np.ndarray = np.array([
            self.__rectangle_controller.push_with_arr(ps)
            for ps in obstacles
        ]).astype(dtype=np.bool8)
        return is_success_arr.all(axis=0)

    def create_wall(
        self, xmin: float, ymin: float,
        xmax: float, ymax: float, width: float
    ) -> bool:
        is_left_wall_success = self.__rectangle_controller.push_with_keys(
            xy=(xmin, ymin), width=width, height=ymax - ymin
        )
        is_upper_wall_success = self.__rectangle_controller.push_with_keys(
            xy=(xmin, ymax - width), width=xmax - xmin, height=width
        )
        is_right_wall_success = self.__rectangle_controller.push_with_keys(
            xy=(xmax - width, ymin), width=width, height=ymax - ymin
        )
        is_bottom_wall_success = self.__rectangle_controller.push_with_keys(
            xy=(xmin, ymin), width=xmax - xmin, height=width
        )
        is_success_arr = np.array([
            is_left_wall_success, is_upper_wall_success,
            is_right_wall_success, is_bottom_wall_success
        ])
        return is_success_arr.all(axis=0)
        
