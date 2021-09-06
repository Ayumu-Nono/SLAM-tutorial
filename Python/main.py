import os
import shutil #ファイル操作

from tqdm import tqdm　#進捗表示

from sequence_manager.initializer import init
from sequence_manager.iterater import each_step

from log.gif.animator import create_gif


if __name__ == "__main__": #メイン文の表明
    
    center, robot, world, picture = init()
    
    shutil.rmtree("log/img") #ディレクトリを中身ごと削除
    os.makedirs("log/img", exist_ok=True)　#ディレクトリを作成
    
    for t in tqdm(range(1, 50)):
        if t % 1 == 0:
            each_step(t, center, robot, world, picture)　#2％ごとに各時間、中心?、ロボット?、世界?、写真?のパラメータとimageファイルの作成

    # closing
    create_gif(inpath=os.path.join("log/img"), outpath="log/gif/animation.gif")
