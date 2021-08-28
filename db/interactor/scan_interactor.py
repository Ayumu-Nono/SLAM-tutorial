from typing import List
from model.scan import Scan
from db.repository.scan_db import ScanDB
from .abstract_interactor import AbstractInteractor


class ScanInteractor(AbstractInteractor):
    def __init__(self) -> None:
        self.__scan_db: ScanDB = ScanDB()

    def push(self, scan: Scan) -> bool:
        assert isinstance(scan, Scan)
        is_success: bool = self.__scan_db.push(scan)
        return is_success

    def get_latest(self) -> Scan:
        assert self.__scan_db.exist()
        return self.__scan_db.get(index=-1)

    def get_2latest(self) -> List[Scan]:
        assert self.__scan_db.get_len() >= 2
        return [self.__scan_db.get(index=-2), self.__scan_db.get(index=-1)]

    def get_all(self):
        raise FutureWarning("Don't use this function")

    def get_len(self) -> int:
        return self.__scan_db.get_len()