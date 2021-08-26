from typing import List
import numpy as np

from model.scan import Scan
from db.interactor.scan_interactor import ScanInteractor


class ScanController:
    def __init__(self) -> None:
        self.__scan_interactor: ScanInteractor = ScanInteractor()

    def push_with_arr(self, data: np.ndarray) -> bool:
        assert isinstance(data, np.ndarray)
        data_as_list: List[tuple] = [
            (row[0], row[1]) for row in data
        ]
        is_success: bool = self.__scan_interactor.push(
            scan=Scan(data=data_as_list)
        )
        return is_success

    def get_latest_scan_as_arr(self) -> np.ndarray:
        scan = self.__scan_interactor.get_latest()
        return np.array(scan)

