from typing import List
from .abstract_db import AbstractDB
from model.command import Command


class CommandDB(AbstractDB):
    def __init__(self) -> None:
        self.__decition_list: List[Command] = []

    def get(self, index: int) -> Command:
        assert isinstance(index, int)
        return self.__decition_list[index]

    def push(self, decision: Command) -> bool:
        assert isinstance(decision, Command)
        old_len: int = len(self.__decition_list)
        self.__decition_list.append(decision)
        return len(self.__decition_list) > old_len

    def exist(self) -> bool:
        return len(self.__decition_list) != 0

    def get_len(self) -> int:
        return len(self.__decition_list)
