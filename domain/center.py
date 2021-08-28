from handler.senser import Senser
from handler.motor import Motor
from handler.commander import Commander


class Center:
    """制御するマン"""
    def __init__(
        self,
        senser: Senser, motor: Motor, commander: Commander
    ) -> None:
        assert isinstance(senser, Senser)
        assert isinstance(motor, Motor)
        assert isinstance(commander, Commander)
        self.__senser: Senser = senser
        self.__motor: Motor = motor
        self.__commander: Commander = commander

    def make_command(self) -> bool:
        is_success = self.__commander.command()
        return is_success

        