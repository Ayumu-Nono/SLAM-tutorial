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

    def smooth_w_scan(
        self, ref_status: Status,
        ref_scan: ScanData, now_scan: ScanData,
        cost_thre=1
    ) -> Status:
        """
            scanデータでスムージング
            args: ref_scan, now_scan
            return: self status
        """
        smtd_status: Status = copy.deepcopy(ref_status)
        cost: float = 1e5
        while (cost >= cost_thre):
            # now_status.change(position=estd_position, angle=estd_angle)
            # score更新

            cost = 0.9
            
        return smtd_status

    def predict_w_odometory(
        self, old_status: Status, now_decision: Decision, dt: float
    ) -> Status:
        """オドメトリで予測"""
        pred_status: Status = copy.deepcopy(old_status)
        old_position: tuple = old_status.position
        old_angle: float = old_status.angle
        dx: float = now_decision.velocity * np.cos(old_angle) * dt
        dy: float = now_decision.velocity * np.sin(old_angle) * dt
        dtheta: float = now_decision.angular_velocity * dt
        estd_position: tuple = (old_position[0] + dx, old_position[1] + dy)
        estd_angle: float = old_angle + dtheta
        pred_status.change(position=estd_position, angle=estd_angle)
        return pred_status
        
        