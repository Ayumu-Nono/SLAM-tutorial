import os
import shutil

import numpy as np

from db.controller.status_controller import StatusController
from db.controller.rectangle_controller import RectangleController
from db.controller.command_controller import CommandController
from db.controller.scan_controller import ScanController
from handler.drawer import Drawer
from handler.creater import Creater
from handler.motor import Motor
from handler.senser import Senser
from handler.commander import Commander
from domain.world import World
from domain.picture import Picture
from domain.robot import Robot
from domain.center import Center

from log.gif.animator import create_gif


if __name__ == "__main__":
    true_status_controller = StatusController()
    rectangle_controller = RectangleController()
    command_controller = CommandController()
    scan_controller = ScanController()
    creater = Creater(rectangle_controller)
    drawer = Drawer(
        rectangle_controller,
        true_status_controller
    )
    motor = Motor(true_status_controller, command_controller)
    senser = Senser(true_status_controller, scan_controller)
    commander = Commander(command_controller)
    # robot.add_motor_noise()

    # Domain
    center = Center(senser, motor, commander)
    robot = Robot(senser, motor)
    world = World(creater)
    pic = Picture(drawer)
    for t in range(0, 50):
        if t == 0:
            robot.set()
            world.set_world()
            shutil.rmtree("log/img")
            os.makedirs("log/img", exist_ok=True)
            pic.save_latest_version(path="log/img/{0:03}.png".format(t))
        else:
            if t % 1 == 0:
                center.control()
                robot.move()
                pic.save_latest_version(path="log/img/{0:03}.png".format(t))

    create_gif(inpath=os.path.join("log/img"), out_filename="animation.gif")
