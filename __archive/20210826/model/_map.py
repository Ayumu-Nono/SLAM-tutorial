import copy
from typing import List, Optional, Tuple

import numpy as np


class Map:
    def __init__(self) -> None:
        """
            segments: array of ((x1, y1), (x2, y2))
        """
        

    def optimize(self, segments: np.ndarray) -> None:
        pass
        

    def update(self, scan_points: np.ndarray) -> None:
        segments: np.ndarray = np.zeros((len(scan_points), 2, 2))
        # make segments
        for i, point in enumerate(scan_points):
            wo_self_scan_points: np.ndarray = scan_points[
                scan_points != point
            ]
            assert len(wo_self_scan_points) == len(scan_points) - 1
            diff: np.ndarray = wo_self_scan_points - point
            norms: np.ndarray = np.linalg.norm(diff, axis=0)
            nearest_point: np.ndarray = wo_self_scan_points[np.argmin(norms)]
            segments[i] = np.array([
                copy.deepcopy(point), copy.deepcopy(nearest_point)
            ])
        self.segments = segments
        # optimize



