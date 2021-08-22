import math

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from model.world import World
from model.world import Rectangle
from model.robot import IdealRobot


def draw(world: World, robot: IdealRobot, outpath: str):
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111)
    ax.set_aspect("equal")
    ax.set_xlim(world.xlim)
    ax.set_ylim(world.ylim)
    rs = [
        patches.Rectangle(xy=rec.xy, width=rec.width, height=rec.height, fc='gray', alpha=0.4)
        for rec in world.obstacles
    ]
    for r in rs:
        ax.add_patch(r)

    # robot
    x, y = robot.position
    x_nose = x + 0.2 * math.cos(robot.angle)
    y_nose = y + 0.2 * math.sin(robot.angle)
    ax.plot([x, x_nose], [y, y_nose], color="green")
    c = patches.Circle(
        xy=(x, y),
        radius=0.2,
        fill=False,
        color="green"
    )
    ax.add_patch(c)
    # scan結果
    scan_points = np.array(robot.see(world=world))
    ax.scatter(scan_points[:, 0], scan_points[:, 1], color="orange")
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
