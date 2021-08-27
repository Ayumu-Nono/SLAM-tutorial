from handler.senser import Senser
from handler.motor import Motor
from params.motor_params import (
    position_noise_rate, angle_noise_rate,
    init_position, init_angle, dt
)


class Robot:
    def __init__(
        self,
        senser: Senser, motor: Motor
    ) -> None:
        assert isinstance(senser, Senser)
        assert isinstance(motor, Motor)
        self.__senser: Senser = senser
        self.__motor: Motor = motor

    def set(self) -> bool:
        is_success: bool = self.__motor.set_init_status(
            position=init_position, angle=init_angle
        )
        return is_success

    def add_motor_noise(self) -> bool:
        is_success: bool = self.__motor.set_noise_rate(
            position_noise_rate, angle_noise_rate
        )
        return is_success

    def move(self) -> bool:
        is_success = self.__motor.move(dt)
        return is_success

    def scan(self) -> bool:
        is_success: bool = self.__senser.scan()
        return is_success
        