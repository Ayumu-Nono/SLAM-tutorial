import math

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from model.world import World
from model.robot import IdealRobot


true_color: str = "black"
true_alpha: float = 0.3
estd_color: str = "green"
estd_alpha: float = 1.0
p_color: str = "blue"
p_alpha: float = 0.7


def draw(world: World, robot: IdealRobot, outpath: str):
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111)
    ax.set_aspect("equal")
    plt.rcParams["font.size"] = 14
    ax.set_xlim(world.xlim)
    ax.set_ylim(world.ylim)
    rs = [
        patches.Rectangle(xy=rec.xy, width=rec.width, height=rec.height, fc='gray', alpha=0.4)
        for rec in world.obstacles
    ]
    for r in rs:
        ax.add_patch(r)

    # robot
    status = robot.storage.robot_true_status_list[-2]
    x, y = status.position
    x_nose = x + 0.3 * math.cos(status.angle)
    y_nose = y + 0.3 * math.sin(status.angle)
    ax.plot([x, x_nose], [y, y_nose], color=true_color, alpha=true_alpha)
    c = patches.Circle(
        xy=(x, y),
        radius=0.2,
        fill=False,
        color=true_color,
        alpha=true_alpha
    )
    ax.add_patch(c)
    # 推定位置
    # 推定するタイミングはoptimizeするタイミングの後なので、1ステップ前を描画してあげる
    estd_status = robot.storage.robot_estd_status_list[-2]
    x, y = estd_status.position
    x_nose = x + 0.3 * math.cos(estd_status.angle)
    y_nose = y + 0.3 * math.sin(estd_status.angle)
    ax.plot([x, x_nose], [y, y_nose], color=estd_color)
    c1 = patches.Circle(
        xy=(x, y),
        radius=0.2,
        fill=False,
        color=estd_color
    )
    ax.add_patch(c1) 
    # particleたち
    for p in robot.estimater.smoother.particles:
        now_status = p
        x, y = now_status.position
        x_nose = x + 0.3 * math.cos(now_status.angle)
        y_nose = y + 0.3 * math.sin(now_status.angle)
        ax.plot([x, x_nose], [y, y_nose], color=p_color)
        c1 = patches.Circle(
            xy=(x, y),
            radius=0.2,
            fill=False,
            color=p_color
        )
        ax.add_patch(c1)
        
    # 軌跡
    xys: np.ndarray = np.array([
        true_status.position
        for true_status in robot.storage.robot_true_status_list[:-1]
    ])
    xys = xys.T
    ax.plot(xys[0], xys[1], color=true_color, alpha=true_alpha, label="true orbit")
    
    xys = np.array([
        estd_status.position
        for estd_status in robot.storage.robot_estd_status_list[:-1]
    ])
    xys = xys.T
    ax.plot(xys[0], xys[1], color=estd_color, alpha=estd_alpha, label="estimated orbit")


    # scan結果
    scan_points = np.array(
        robot.see(world=world).get_as_cartesian(
            self_position=robot.status.position,
            self_angle=robot.status.angle
        )
    )
    ax.scatter(scan_points[:, 0], scan_points[:, 1], color="orange")
    # 推定スキャン
    scan_points = np.array(
        robot.see(world=world).get_as_cartesian(
            self_position=estd_status.position,
            self_angle=estd_status.angle
        )
    )
    ax.scatter(scan_points[:, 0], scan_points[:, 1], fc="white", ec="black")
    plt.legend()
    fig.savefig(outpath)
    plt.close()
