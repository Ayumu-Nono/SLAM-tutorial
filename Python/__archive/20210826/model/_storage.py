from typing import List, Optional
import copy

from ._status import Status
from ._senser import ScanData
from ._pilot import Decision


class Storage:
    def __init__(self) -> None:
        self.robot_true_status_list: List[Status] = []
        self.robot_estd_status_list: List[Status] = []
        self.scan_data_list: List[ScanData] = []
        self.decision_list: List[Decision] = []

    def store(
        self,
        robot_true_status: Optional[Status],
        robot_estd_status: Optional[Status],
        scan_data: Optional[ScanData],
        decision: Optional[Decision]
    ) -> dict:
        if robot_true_status is not None:
            self.robot_true_status_list.append(copy.deepcopy(robot_true_status))
        if robot_estd_status is not None:
            self.robot_estd_status_list.append(copy.deepcopy(robot_estd_status))
        if scan_data is not None:
            self.scan_data_list.append(copy.deepcopy(scan_data))
        if decision is not None:
            self.decision_list.append(copy.deepcopy(decision))
        storage_status: dict = {
            "robot_true_status": len(self.robot_true_status_list),
            "robot_estd_status": len(self.robot_estd_status_list),
            "scan_data_list": len(self.scan_data_list),
            "decision_list": len(self.decision_list)
        }
        return storage_status

 