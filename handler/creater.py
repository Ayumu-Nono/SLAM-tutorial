import numpy as np

from db.controller.rectangle_controller import RectangleController


class Creater:
    """世界を創造するマン"""
    def __init__(
        self,
        rectangle_controller: RectangleController
    ) -> None:
        self.__rectangle_controller: RectangleController = rectangle_controller

    def create_obstacles(self, obstacles: np.ndarray) -> int:
        """(rectangle数, 点の数, 座標)の3次元"""
        assert obstacles.ndim == 3
        nums: np.ndarray = np.array([
            self.__rectangle_controller.push_with_arr(ps)
            for ps in obstacles
        ]).astype(dtype=np.int32)
        return int(np.max(nums))

    def create_wall(
        self, xmin: float, ymin: float,
        xmax: float, ymax: float, width: float
    ) -> int:
        assert width > 0
        assert xmin < xmax
        assert ymin < ymax
        num = self.__rectangle_controller.push_with_keys(
            xy=(xmin - width, ymin), width=width, height=ymax - ymin
        )
        num = self.__rectangle_controller.push_with_keys(
            xy=(xmin, ymax), width=xmax - xmin, height=width
        )
        num = self.__rectangle_controller.push_with_keys(
            xy=(xmax, ymin), width=width, height=ymax - ymin
        )
        num = self.__rectangle_controller.push_with_keys(
            xy=(xmin, ymin - width), width=xmax - xmin, height=width
        )
        return num

