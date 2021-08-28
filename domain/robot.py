from handler.senser import Senser
from handler.motor import Motor
from params.motor_params import (
    position_noise_rate, angle_noise_rate,
    init_position, init_angle, dt
)
from params.senser_params import n_laser


class Robot:
    def __init__(
        self,
        senser: Senser, motor: Motor
    ) -> None:
        assert isinstance(senser, Senser)
        assert isinstance(motor, Motor)
        self.__senser: Senser = senser
        self.__motor: Motor = motor

    def move(self) -> bool:
        is_success = self.__motor.move(dt)
        return is_success

    def see(self) -> bool:
        is_success: bool = self.__senser.scan(n_laser)
        return is_success

