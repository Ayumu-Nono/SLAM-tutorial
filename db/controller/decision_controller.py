import numpy as np

from model.decision import Decision
from db.interactor.decision_interactor import DecisionInteractor


class DecisionController:
    def __init__(self) -> None:
        self.__decision_interactor: DecisionInteractor = DecisionInteractor()

    def push_with_float(self, velocity: float, angular_velocity: float) -> bool:
        assert isinstance(velocity, float)
        assert isinstance(angular_velocity, float)
        decision: Decision = Decision(
            velocity=velocity, angular_velocity=angular_velocity
        )
        is_success: bool = self.__decision_interactor.push(decision=decision)
        return is_success

    def get_latest_velocity_as_float(self) -> float:
        decision: Decision = self.__decision_interactor.get_latest()
        return decision.velocity

    def get_latest_angular_velocity_as_float(self) -> float:
        decision: Decision = self.__decision_interactor.get_latest() 
        return decision.angular_velocity
