from typing import List

import numpy as np


class Pilot:
    def __init__(self) -> None:
        pass

    def decide(
        self, position: tuple, angle: float, scan_points: List[tuple]
    ) -> tuple:
        """
            args:
            return: (velocity, angular_velocity)
        """
        ps: np.ndarray = np.array(scan_points)
        p0s: np.ndarray = np.tile(position, (len(ps), 1))
        diff: np.ndarray = ps - p0s
        thetas: np.ndarray = np.arctan2(diff[:, 1], diff[:, 0])
        # 進んでる向きと一番近い角度はどれ？
        i_head = np.argmin(np.abs(thetas - angle))
        i_right = np.argmin(np.abs(thetas - angle - np.pi / 4))
        distances: np.ndarray = np.linalg.norm(diff, axis=1)
        # 進んでる向きの距離
        d_head: float = distances[i_head]
        d_right: float = distances[i_right]
        
        if d_head < 1:
            decision = (2, np.pi / 4 / 0.01)
        # elif 1 <= d_head and d_head < 2 and 1 < d_right:
            # decision = (1, - np.pi / 4 / 0.01)
        elif 1 <= d_head and d_head < 2:
            decision = (5, 0)
        else:
            decision = (30, 0)
        return decision
        
