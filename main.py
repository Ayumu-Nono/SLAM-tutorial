import os
import shutil

from sequence_manager.initializer import init
from log.gif.animator import create_gif


if __name__ == "__main__":
    for t in range(0, 50):
        if t == 0:
            center, robot, world, picture = init()
            shutil.rmtree("log/img")
            os.makedirs("log/img", exist_ok=True)
            picture.save_latest_version(path="log/img/{0:03}.png".format(t))
        else:
            if t % 1 == 0:
                center.estimate_wo_scan()
                robot.see()
                center.make_command()
                picture.save_latest_version(path="log/img/{0:03}.png".format(t))
                robot.move()

    # closing
    create_gif(inpath=os.path.join("log/img"), outpath="log/gif/ animation.gif")
