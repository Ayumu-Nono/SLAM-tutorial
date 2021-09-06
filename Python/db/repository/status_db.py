from typing import List
from .abstract_db import AbstractDB
from model.status import Status


class StatusDB(AbstractDB):
    def __init__(self) -> None:
        self.__status_list: List[Status] = []

    def get(self, index: int) -> Status:
        assert isinstance(index, int)
        return self.__status_list[index]

    def push(self, status: Status) -> bool:
        assert isinstance(status, Status)
        old_len: int = len(self.__status_list)
        self.__status_list.append(status)
        return len(self.__status_list) > old_len

    def exist(self) -> bool:
        return len(self.__status_list) != 0
    
    def get_len(self) -> int:
        return len(self.__status_list)
        
