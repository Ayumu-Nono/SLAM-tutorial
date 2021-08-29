from typing import Tuple

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
from handler.predicter import Predicter
from handler.smoother import Smoother
from domain.world import World
from domain.picture import Picture
from domain.robot import Robot
from domain.center import Center

from params.motor_params import (
    init_position, init_angle, position_noise_rate, angle_noise_rate
)
from params.commander_params import init_velocity, init_angular_velocity
from params.senser_params import n_laser


def init() -> Tuple[Center, Robot, World, Picture]:
    np.random.seed(seed=10)
    # Controllers
    true_status_controller = StatusController()
    pred_status_controller = StatusController()
    smtd_status_controller = StatusController()
    scan_controller = ScanController()
    rectangle_controller = RectangleController()
    command_controller = CommandController()
    # Handlers
    creater = Creater(rectangle_controller)
    drawer = Drawer(
        rectangle_controller,
        true_status_controller,
        pred_status_controller,
        smtd_status_controller,
        scan_controller
    )
    motor = Motor(true_status_controller, command_controller)
    senser = Senser(
        true_status_controller, scan_controller, rectangle_controller
    )
    commander = Commander(command_controller)
    predicter = Predicter(
        pred_status_controller=pred_status_controller,
        smtd_status_controller=smtd_status_controller,
        command_controller=command_controller
    )
    smoother = Smoother(
        pred_status_controller=pred_status_controller,
        smtd_status_controller=smtd_status_controller,
        scan_controller=scan_controller
    )
    # Domains
    center = Center(senser, motor, commander, predicter, smoother)
    robot = Robot(senser, motor)
    world = World(creater)
    picture = Picture(drawer)

    # init
    world.set_world()
    motor.set_noise_rate(position_noise_rate, angle_noise_rate)
    _t1 = motor.set_initial_status(init_position, init_angle)
    _t2 = predicter.set_initial_status(init_position, init_angle)
    _t3 = senser.scan(n_laser)
    _t4 = smoother.set_initial_status(init_position, init_angle)
    _t5 = commander.set_initial_command(init_velocity, init_angular_velocity)
    _ts = np.array([_t1, _t2, _t3, _t4, _t5])
    assert np.all(_ts == np.ones(len(_ts))), _ts

    picture.save_latest_version(path="log/img/{0:03}.png".format(0))
    
    return center, robot, world, picture
