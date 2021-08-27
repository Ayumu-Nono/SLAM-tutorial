from handler.senser import Senser
from handler.motor import Motor
from params.motor_params import position_noise_rate, angle_noise_rate


class Robot:
    def __init__(
        self,
        senser: Senser, motor: Motor
    ) -> None:
        assert isinstance(senser, Senser)
        assert isinstance(motor, Motor)
        self.__senser: Senser = senser
        self.__motor: Motor = motor

    def add_motor_noise(self) -> bool:
        is_success: bool = self.__motor.set_noise_rate(
            position_noise_rate, angle_noise_rate
        )
        return is_success



    def scan(self) -> bool:
        is_success: bool = self.__senser.scan()
        return is_success
        