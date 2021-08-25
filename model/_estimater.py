from typing import List
import copy

import numpy as np

from ._senser import ScanData
from ._status import Status
from ._optimizer import Optimizer
from ._pilot import Decision


class Smoother:
    """scanデータを用いてスムージングします"""
    def __init__(self) -> None:
        self.ref_status: Status = None
        self.ref_scan_data: ScanData = None
        self.now_scan_data: ScanData = None
        self.particles: List[Status] = []
        self.is_import_done: bool = False
    
    def _import_data(self, ref_status: Status, ref_scan_data: ScanData, now_scan_data) -> None:
        self.ref_status = copy.deepcopy(ref_status)
        self.ref_scan_data = copy.deepcopy(ref_scan_data)
        self.now_scan_data = copy.deepcopy(now_scan_data)
        self.is_import_done = True
    
    def _make_pair_array(
        self, ref_points: np.ndarray, now_points: np.ndarray
    ) -> np.ndarray:
        """
            sizeが(any, 2)のarray2組を対応づけてsizeが(any, 4)のarrayを返す
            最も近い点を紐づける
        """
        refs: np.ndarray = copy.deepcopy(ref_points)
        nows: np.ndarray = copy.deepcopy(now_points)
        sorted_refs: np.ndarray = np.array([
            refs[np.argmin(np.linalg.norm(now - refs, axis=1))]
            for now in nows
        ])
        pair_array: np.ndarray = np.hstack([nows, sorted_refs])
        return pair_array

    def _get_pair_array(self, now_status: Status) -> np.ndarray:
        """
            referenceデータと対応づける
            sizeは(any, 4)で[:2]がnowで[3:]がref
        """
        ref_scan_points: np.ndarray = np.array(
            self.ref_scan_data.get_as_cartesian(
                self_position=self.ref_status.position,
                self_angle=self.ref_status.angle
            )
        )
        now_scan_points: np.ndarray = np.array(
            self.now_scan_data.get_as_cartesian(
                self_position=now_status.position,
                self_angle=now_status.angle
            )
        )
        pair_array: np.ndarray = self._make_pair_array(
            ref_points=ref_scan_points, now_points=now_scan_points
        )
        return pair_array

    def _calc_score(self, pair_array: np.ndarray) -> float:
        """logとった方がいいね"""
        diffs: np.ndarray = pair_array[:, :2] - pair_array[:, 3:]
        norms: np.ndarray = np.linalg.norm(diffs, axis=1)
        x = np.mean(norms)
        score: float = np.exp(-x)
        return score

    def _score_function(self, status: Status) -> float:
        pair_array: np.ndarray = self._get_pair_array(now_status=status)
        score: float = self._calc_score(pair_array=pair_array)
        return score

    def smooth(
        self, init_status: Status, now_scan_data: ScanData,
        ref_status: Status, ref_scan_data: ScanData,
    ) -> Status:
        self._import_data(
            ref_status=ref_status,
            ref_scan_data=ref_scan_data,
            now_scan_data=now_scan_data
        )
        optimizer = Optimizer(init_status=init_status)
        optimizer.set_score_function(func=self._score_function)
        optimizer.optimize()
        self.particles = optimizer.particles
        return optimizer.opzd_status
        # return now_status

    


class Estimater:
    """自分の位置を推定します"""
    def __init__(self) -> None:
        self.smoother: Smoother = Smoother()


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
        now_status: Status = copy.deepcopy(ref_status)

        now_status = self.smoother.smooth(
            init_status=now_status, now_scan_data=now_scan,
            ref_status=ref_status, ref_scan_data=ref_scan,
        )    
        return now_status