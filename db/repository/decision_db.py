from typing import List
from .abstract_db import AbstractDB
from model.decision import Decision


class DecisionDB(AbstractDB):
    def __init__(self) -> None:
        self.__decition_list: List[Decision] = []

    def get(self, index: int) -> Decision:
        assert isinstance(index, int)
        return self.__decition_list[index]

    def push(self, decision: Decision) -> bool:
        assert isinstance(decision, Decision)
        old_len: int = len(self.__decition_list)
        self.__decition_list.append(decision)
        return len(self.__decition_list) > old_len

    def exist(self) -> bool:
        return len(self.__decition_list) != 0

    def get_len(self) -> int:
        return len(self.__decition_list)
