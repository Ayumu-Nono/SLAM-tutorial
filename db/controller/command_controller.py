from model.command import Command
from db.interactor.command_interactor import CommandInteractor


class CommandController:
    def __init__(self) -> None:
        self.__decision_interactor: CommandInteractor = CommandInteractor()

    def push_with_float(
        self, velocity: float, angular_velocity: float
    ) -> bool:
        assert isinstance(velocity, float)
        assert isinstance(angular_velocity, float)
        decision: Command = Command(
            velocity=velocity, angular_velocity=angular_velocity
        )
        is_success: bool = self.__decision_interactor.push(decision=decision)
        return is_success

    def get_latest_velocity_as_float(self) -> float:
        decision: Command = self.__decision_interactor.get_latest()
        return decision.velocity

    def get_latest_angular_velocity_as_float(self) -> float:
        decision: Command = self.__decision_interactor.get_latest() 
        return decision.angular_velocity
