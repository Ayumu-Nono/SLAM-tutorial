import os
import shutil

from tqdm import tqdm

from sequence_manager.initializer import init
from sequence_manager.iterater import each_step

from log.gif.animator import create_gif


if __name__ == "__main__":
    center, robot, world, picture = init()
    shutil.rmtree("log/img")
    os.makedirs("log/img", exist_ok=True)
    
    for t in tqdm(range(1, 50)):
        if t % 1 == 0:
            each_step(t, center, robot, world, picture)

    # closing
    create_gif(inpath=os.path.join("log/img"), outpath="log/gif/animation.gif")
