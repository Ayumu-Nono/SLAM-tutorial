from typing import List
from .abstract_db import AbstractDB
from model.scan import Scan


class ScanDB(AbstractDB):
    def __init__(self) -> None:
        self.__scan_list: List[Scan] = []

    def get(self, index: int) -> Scan:
        assert isinstance(index, int)
        return self.__scan_list[index]

    def push(self, scan: Scan) -> bool:
        assert isinstance(scan, Scan)
        old_len: int = len(self.__scan_list)
        self.__scan_list.append(scan)
        return len(self.__scan_list) > old_len

    def exist(self) -> bool:
        return len(self.__scan_list) != 0
    
    def get_len(self) -> int:
        return len(self.__scan_list)
        