from typing import Tuple

import numpy as np

from domain.world import World
from domain.picture import Picture
from domain.robot import Robot
from domain.center import Center


def each_step(
    t: int,
    center: Center, robot: Robot, world: World, picture: Picture
) -> Tuple[Center, Robot, World, Picture]:
    _t1 = robot.move()
    _t2 = center.estimate_wo_scan()
    _t3 = robot.see()
    _t4 = center.estimate_w_scan()
    _t5 = center.make_command()
    _ts = np.array([_t1, _t2, _t3, _t4, _t5])
    assert np.all(_ts == np.tile(t + 1, len(_ts))), _ts

    picture.save_latest_version(path="log/img/{0:03}.png".format(t))

    return center, robot, world, picture
