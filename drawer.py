from typing import List
import itertools

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from model.world import World
from model.world import Rectangle
from model.robot import IdealRobot


def draw(world: World, robot: IdealRobot, outpath: str):
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111)
    ax.set_xlim(world.xlim)
    ax.set_ylim(world.ylim)
    rs = [
        patches.Rectangle(xy=rec.xy, width=rec.width, height=rec.height, fc='gray', alpha=0.4)
        for rec in world.obstacles
    ]
    for r in rs:
        ax.add_patch(r)

    # robot
    ax.scatter(robot.position[0], robot.position[1], color="red", s=100)
    # scan結果
    _segments = [
        obs.segments
        for obs in world.obstacles
    ]
    segments: list = list(itertools.chain.from_iterable(_segments))
    scan_points: List[tuple] = robot.senser.scan(
        position=robot.position,
        segments=segments
    )
    for point in scan_points:
        ax.scatter(point[0], point[1], color="orange", zorder=3)
    fig.savefig(outpath)


if __name__ == "__main__":
    ayumu1 = IdealRobot(position=(4, 1), velocity=0, angle=0)
    stage1 = World(
        obstacles=[
            Rectangle(xy=(1, 1), width=1, height=2),
            Rectangle(xy=(5, 0), width=1, height=8),
            Rectangle(xy=(0, 0), width=10, height=0.1),
            Rectangle(xy=(9.9, 0), width=0.1, height=10),
            Rectangle(xy=(0, 9.9), width=10, height=0.1),
            Rectangle(xy=(0, 0), width=0.1, height=10)
        ]
    )
    draw(world=stage1, robot=ayumu1, outpath="world.png")
