from typing import List
from model.scan import Scan
from db.repository.scan_db import ScanDB


class ScanInteractor:
    def __init__(self) -> None:
        self.__scan_db: ScanDB = ScanDB()

    def push(self, scan: Scan) -> bool:
        assert isinstance(scan, Scan)
        is_success: bool = self.__scan_db.push(scan)
        return is_success

    def get_latest_scan(self) -> Scan:
        assert self.__scan_db.exist()
        return self.__scan_db.get(index=-1)

    def get_2latest_scan(self) -> List[Scan]:
        assert self.__scan_db.get_len() >= 2
        return [self.__scan_db.get(index=-2), self.__scan_db.get(index=-1)]