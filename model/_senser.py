import math
from typing import List, Optional, Tuple

import numpy as np

from ._parameter import num_senser_light


def _reflect(
    half_line: Tuple[tuple, tuple], segment: Tuple[tuple, tuple]
) -> Tuple[tuple, tuple]:
    """
        args:
            half_line: レーザーの半直線. (x1, y1)起点で(x2, y2)を通る
            segment: 壁の線分
        return:
            交点かNone
    """
    x1, y1 = half_line[0]
    x2, y2 = half_line[1]
    x3, y3 = segment[0]
    x4, y4 = segment[1]
    assert x1 != x2 or y1 != y2
    assert x3 != x4 or y3 != y4
    a = np.zeros((2, 2))
    b = np.zeros(2)
    a[0, 0] = - (y2 - y1)
    a[0, 1] = x2 - x1
    a[1, 0] = - (y4 - y3)
    a[1, 1] = x4 - x3
    b[0] = y1 * (x2 - x1) - x1 * (y2 - y1)
    b[1] = y3 * (x4 - x3) - x3 * (y4 - y3)
    if np.linalg.matrix_rank(a) != len(a):
        result = (np.nan, np.nan)
    else:
        x, y = np.linalg.solve(a, b)
        result = (x, y)
        # 半直線条件
        if (x - x1) * (x2 - x1) < 0 or (y - y1) * (y2 - y1) < 0:
            result = (np.nan, np.nan)
        # 線分条件
        if (x3 - x) * (x4 - x) > 0 or (y3 - y) * (y4 - y) > 0:
            result = (np.nan, np.nan)
    return result


def _irradiate(position: tuple, angle: float) -> Tuple[tuple, tuple]:
    """
        args:
            position: どこから
            angle: どの向きに
        return: p1が起点でp2を通る半直線
    """
    p1: tuple = position
    p2: tuple = (
        position[0] + math.cos(angle),
        position[1] + math.sin(angle)
    )
    half_line: Tuple[tuple, tuple] = (p1, p2)
    return half_line


def _receive(
        half_line: Tuple[tuple, tuple], segments: List[Tuple[tuple, tuple]]
) -> tuple:
    x1, y1 = half_line[0]
    """最も近い壁の反射だけが見えるよね"""
    distances: np.ndarray = np.zeros(len(segments))
    results: List[Tuple[tuple, tuple]] = [
        _reflect(half_line=half_line, segment=segment)
        for segment in segments
    ]

    for i, result in enumerate(results):
        _p1 = np.array(result)
        if not np.isnan(_p1).any():
            _p2 = np.array([x1, y1])
            distances[i] = np.linalg.norm(_p1 - _p2)
        else:
            distances[i] = np.inf
    i_nearest: int = int(np.argmin(distances))
    return results[i_nearest]


class ScanData:
    """
        raw: (distance, angle)
            distance: ロボットからの距離
            angle: ロボットからみた角度。正面が0[rad]
        points: (x, y)
    """
    def __init__(self, raw: List[tuple]) -> None:
        self.raw: List[tuple] = raw

    def get_as_polar(self, self_position: tuple) -> List[tuple]:
        return self.raw

    def get_as_cartesian(
        self, self_position: tuple, self_angle: float
    ) -> List[tuple]:
        """直交座標で取得"""
        ds: np.ndarray = np.array(self.raw)[:, 0]
        angles: np.ndarray = np.array(self.raw)[:, 1]
        xs: np.ndarray = ds * np.cos(angles + self_angle) + self_position[0]
        ys: np.ndarray = ds * np.sin(angles + self_angle) + self_position[1]
        assert len(xs) == len(ys)
        points: List[tuple] = [
            (xs[i], ys[i]) for i in range(len(xs))
        ]
        return points


class IdealSenser:
    def __init__(self) -> None:
        pass

    def scan(
        self, self_position: tuple, self_angle: float,
        segments: List[Tuple[tuple, tuple]]
    ) -> ScanData:
        angles: np.ndarray = np.linspace(-np.pi, np.pi, num_senser_light)
        scan_points: List[tuple] = [
            _receive(
                half_line=_irradiate(position=self_position, angle=angle),
                segments=segments
            )
            for angle in angles
        ]
        assert len(scan_points) == len(angles)
        distances: np.ndarray = np.linalg.norm(
            np.array(scan_points) - self_position,
            axis=1
        )
        scan_data: ScanData = ScanData(
            raw=[
                (distances[i], angle - self_angle)  # robotから見た角度
                for i, angle in enumerate(angles)
            ]
        )
        return scan_data
