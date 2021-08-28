from handler.senser import Senser
from handler.motor import Motor
from handler.commander import Commander
from handler.predicter import Predicter
from handler.smoother import Smoother
from params.hyper_params import dt


class Center:
    """制御するマン"""
    def __init__(
        self,
        senser: Senser, motor: Motor, commander: Commander,
        predicter: Predicter, smoother: Smoother
    ) -> None:
        assert isinstance(senser, Senser)
        assert isinstance(motor, Motor)
        assert isinstance(commander, Commander)
        assert isinstance(predicter, Predicter)
        assert isinstance(smoother, Smoother)
        self.__senser: Senser = senser
        self.__motor: Motor = motor
        self.__commander: Commander = commander
        self.__predicter: Predicter = predicter
        self.__smoother: Smoother = smoother

    def make_command(self) -> bool:
        is_success = self.__commander.command()
        return is_success

    def estimate_wo_scan(self) -> bool:
        is_success = self.__predicter.predict(dt)
        return is_success
