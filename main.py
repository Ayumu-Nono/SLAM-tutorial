import os
import shutil

from tqdm import tqdm

from drawer import draw
from animater import create_gif
from model.world import World
from model.world import Rectangle
from model.robot import IdealRobot


ayumu1 = IdealRobot(position=(0.5, 0.5), angle=3.14 / 2)
stage1 = World(
    obstacles=[
        Rectangle(xy=(1, 5), width=3, height=2),
        Rectangle(xy=(1, 1), width=1, height=2),
        Rectangle(xy=(5, 0), width=1, height=8),
        Rectangle(xy=(0, 0), width=10, height=0.1),
        Rectangle(xy=(9.9, 0), width=0.1, height=10),
        Rectangle(xy=(0, 9.9), width=10, height=0.1),
        Rectangle(xy=(0, 0), width=0.1, height=10)
    ]
)


dir = "img"
shutil.rmtree(dir)
os.makedirs(dir, exist_ok=True)

for t in tqdm(range(20)):
    ayumu1.each_step(t=t, world=stage1)
    if t % 1 == 0:
        outpath = os.path.join(dir, "{0:03}.png".format(t))
        if t > 0:
            draw(world=stage1, robot=ayumu1, outpath=outpath)

create_gif(out_filename="animation.gif")
