from typing import List
import copy

from ._senser import ScanData
from ._status import Status


class Estimater:
    """自分の位置を推定します"""
    def __init__(self) -> None:
        pass

    def estimate(
        self, ref_status: Status, ref_scan: ScanData, now_scan: ScanData,
        cost_thre=1
    ) -> Status:
        """
            args: ref_scan, now_scan
            return: self status
        """
        now_status: Status = copy.deepcopy(ref_status)
        cost: float = 1e5
        while (cost >= cost_thre):
            old_position: tuple = ref_status.position
            old_angle: float = ref_status.angle
            now_status.change(position=(old_position[0] + 1, old_position[1]), angle=None)
            # score更新

            cost = 0.9
            
        return now_status
        
        