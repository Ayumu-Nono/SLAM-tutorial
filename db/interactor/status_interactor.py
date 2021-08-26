from typing import List
from model.status import Status
from db.repository.status_db import StatusDB


class StatusInteractor:
    def __init__(self) -> None:
        self.__status_db: StatusDB = StatusDB()

    def push(self, status: Status) -> bool:
        assert isinstance(status, Status)
        is_success: bool = self.__status_db.push(status)
        return is_success
        
    def get_latest_status(self) -> Status:
        assert self.__status_db.exist()
        return self.__status_db.get(index=-1)
    
    def get_2latest_status(self) -> List[Status]:
        assert self.__status_db.get_len() >= 2
        return [self.__status_db.get(index=-2), self.__status_db.get(index=-2)]

