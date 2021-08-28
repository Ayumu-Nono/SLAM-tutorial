import numpy as np

from db.controller.status_controller import StatusController
from db.controller.command_controller import CommandController


class Predicter:
    def __init__(
        self,
        pred_status_controller: StatusController,
        smtd_status_controller: StatusController,
        command_controller: CommandController
    ) -> None:
        self.__pred_status_controller: StatusController = pred_status_controller
        self.__smtd_status_controller: StatusController = smtd_status_controller
        self.__command_controller: CommandController = command_controller

    def set_initial_status(self, position: np.ndarray, angle: float) -> int:
        assert self.__pred_status_controller.get_latest_tstep_as_int() == 0
        t: int = self.__pred_status_controller.push_with_arr(position, angle)
        return t 

    def predict(self, dt: float) -> int:
        old_positon = self.__smtd_status_controller.get_latest_position_as_arr()
        old_angle = self.__smtd_status_controller.get_latest_angle_as_float()
        now_velocity = self.__command_controller.get_latest_velocity_as_float()
        now_angular_v = self.__command_controller.get_latest_angular_velocity_as_float()
        dx = now_velocity * np.cos(old_angle) * dt
        dy = now_velocity * np.sin(old_angle) * dt
        d_theta = now_angular_v * dt
        now_position = old_positon + np.array([dx, dy])
        now_angle = old_angle + d_theta
        t: int = self.__pred_status_controller.push_with_arr(now_position, now_angle)
        return t 

        

        

    