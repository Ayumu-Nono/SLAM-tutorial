from typing import List
import copy

import numpy as np

from ._senser import ScanData
from ._status import Status
from ._pilot import Decision


class Estimater:
    """自分の位置を推定します"""
    def __init__(self) -> None:
        pass

    def estimate(
        self, ref_status: Status,
        ref_scan: ScanData, now_scan: ScanData,
        old_decision: Decision,
        dt: float, cost_thre=1
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
            dx: float = old_decision.velocity * np.cos(old_angle) * dt
            dy: float = old_decision.velocity * np.sin(old_angle) * dt
            dtheta: float = old_decision.angular_velocity * dt
            estd_position: tuple = (old_position[0] + dx, old_position[1] + dy)
            estd_angle: float = old_angle + dtheta
            now_status.change(position=estd_position, angle=estd_angle)
            # score更新

            cost = 0.9
            
        return now_status
        
        