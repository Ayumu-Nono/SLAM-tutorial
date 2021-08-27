from handler.creater import Creater
from params.world_params import xmin, xmax, ymin, ymax, obstacles, wall_width


class World:
    def __init__(self, creater: Creater) -> None:
        assert isinstance(creater, Creater)
        self.__creater: Creater = creater

    def set_world(self) -> bool:
        is_obs_success: bool = self.__creater.create_obstacles(obstacles)
        is_wall_success: bool = self.__creater.create_wall(
            xmin, ymin, xmax, ymax, wall_width
        )
        return is_obs_success and is_wall_success
