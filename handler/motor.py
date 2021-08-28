import numpy as np
from numpy.random import randn

from db.controller.status_controller import StatusController
from db.controller.command_controller import CommandController


class Motor:
    """位置制御するひと"""
    def __init__(
        self,
        status_controller: StatusController,
        command_controller: CommandController
    ) -> None:
        self.__status_controller: StatusController = status_controller
        self.__command_controller: CommandController = command_controller
        self.__position_noise_rate: float = 0.0
        self.__angle_noise_rate: float = 0.0

    def set_initial_status(self, position: np.ndarray, angle: float) -> bool:
        assert self.__status_controller.get_latest_tstep_as_int() == 0
        is_success = self.__status_controller.push_with_arr(position, angle)
        return is_success

    def set_noise_rate(
        self,
        position_noise_rate: float,
        angle_noise_rate: float
    ) -> bool:
        self.__position_noise_rate = position_noise_rate
        self.__angle_noise_rate = angle_noise_rate
        return True
        
    def move(self, dt: float) -> bool:
        old_position = self.__status_controller.get_latest_position_as_arr()
        old_angle = self.__status_controller.get_latest_angle_as_float()
        velocity = self.__command_controller.get_latest_velocity_as_float()
        angular_velocity \
            = self.__command_controller.get_latest_angular_velocity_as_float()
        dx = velocity * np.cos(old_angle) * dt
        dy = velocity * np.sin(old_angle) * dt
        d_position = np.array([dx, dy])
        d_angle = angular_velocity * dt
        new_position = old_position + d_position
        new_angle = old_angle + d_angle
        # noise
        new_position += randn() * self.__position_noise_rate * d_position
        new_angle += randn() * self.__angle_noise_rate * d_angle
        is_success: bool = self.__status_controller.push_with_arr(
            position=new_position, angle=new_angle
        )
        return is_success

