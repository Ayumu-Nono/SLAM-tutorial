from typing import List
from model.decision import Decision
from db.repository.decision_db import DecisionDB
from interactor.abstract_interactor import AbstractInteractor


class DecisionInteractor(AbstractInteractor):
    def __init__(self) -> None:
        self.__decision_db: DecisionDB = DecisionDB

    def push(self, decision: Decision) -> bool:
        assert isinstance(decision, Decision)
        is_success: bool = self.__decision_db.push(decision)
        return is_success

    def get_latest(self) -> Decision:
        assert self.__decision_db.exist()
        return self.__decision_db.get(index=-1)
