import numpy as np

from db.controller.rectangle_controller import RectangleController


class Creater:
    """世界を創造するマン"""
    def __init__(
        self,
        rectangle_controller: RectangleController
    ) -> None:
        self.__rectangle_controller: RectangleController = rectangle_controller

    def create_obstacles(self, obstacles: np.ndarray) -> int:　#obstaclesは(rectangle数, 点の数, 座標)の3次元
        """(rectangle数, 点の数, 座標)の3次元"""
        assert obstacles.ndim == 3　#前提条件
        nums: np.ndarray = np.array([
            self.__rectangle_controller.push_with_arr(ps) #ps配列から四角形の辺の長さを計算
            for ps in obstacles
        ]).astype(dtype=np.int32)
        return int(np.max(nums))

    def create_wall(　#四辺の壁の座標を壁の厚さを含めて算出
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

