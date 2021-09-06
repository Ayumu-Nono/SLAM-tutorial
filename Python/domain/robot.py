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

    def move(self) -> int:
        t: int = self.__motor.move(dt)
        return t 

    def see(self) -> int:
        t: int = self.__senser.scan(n_laser)
        return t 

