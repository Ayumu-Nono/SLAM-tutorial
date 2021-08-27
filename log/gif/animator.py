import os

from PIL import Image
from glob import glob


def create_gif(inpath: str, out_filename):
    path_list = sorted(glob(os.path.join(inpath, "*png")))
    imgs = []
    for i in range(len(path_list)):
        img = Image.open(path_list[i])
        imgs.append(img)
    imgs[0].save(
        out_filename, save_all=True,
        append_images=imgs[1:], optimize=False, duration=100, loop=0
    )

