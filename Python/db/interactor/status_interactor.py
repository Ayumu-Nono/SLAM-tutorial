from typing import List
from model.status import Status
from db.repository.status_db import StatusDB
from .abstract_interactor import AbstractInteractor


class StatusInteractor(AbstractInteractor):
    def __init__(self) -> None:
        self.__status_db: StatusDB = StatusDB()

    def push(self, status: Status) -> bool:
        assert isinstance(status, Status)
        is_success: bool = self.__status_db.push(status)
        return is_success
        
    def get_latest(self) -> Status:
        assert self.__status_db.exist()
        return self.__status_db.get(index=-1)

    def get_2ndlatest(self) -> Status:
        assert self.__status_db.get_len() >= 2
        return self.__status_db.get(index=-2)
    
    def get_2latest(self) -> List[Status]:
        assert self.__status_db.get_len() >= 2
        return [self.__status_db.get(index=-2), self.__status_db.get(index=-1)]

    def get_all(self) -> List[Status]:
        assert self.__status_db.exist()
        return [
            self.__status_db.get(i) for i in range(self.__status_db.get_len())
        ]

    def get_len(self) -> int:
        return self.__status_db.get_len()
