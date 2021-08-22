import pandas as pd

from drawer import draw
from model.world import World
from model.world import Rectangle
from model.robot import IdealRobot


df = pd.read_csv("test.csv")
print(df)

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

for i in range(len(df)):
    outpath = "img/{0}.png".format(df.loc[i, "t"])
    ayumu1.position = (df.loc[i, "x"], df.loc[i, "y"])
    draw(world=stage1, robot=ayumu1, outpath=outpath)
    
