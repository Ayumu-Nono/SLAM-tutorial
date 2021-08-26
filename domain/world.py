import numpy as np

from handler.creater import Creater


class World:
    def __init__(self, creater: Creater) -> None:
        assert isinstance(creater, Creater)
        self.__creater: Creater = creater

    def set_world(
        self, obstacles: np.ndarray,
        xmin: float, ymin: float, xmax: float, ymax: float, width: float
    ) -> bool:
        is_obs_success: bool = self.__creater.create_obstacles(obstacles)
        is_wall_success: bool = self.__creater.create_wall(
            xmin, ymin, xmax, ymax, width
        )
        return is_obs_success and is_wall_success
