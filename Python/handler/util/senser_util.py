import numpy as np


def _reflect(
    half_line: np.ndarray, segment: np.ndarray
) -> np.ndarray:
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
        result = np.array([np.nan, np.nan])
    else:
        x, y = np.linalg.solve(a, b)
        result = np.array([x, y])
        # 半直線条件
        if (x - x1) * (x2 - x1) < 0 or (y - y1) * (y2 - y1) < 0:
            result = np.array([np.nan, np.nan])
        # 線分条件
        if (x3 - x) * (x4 - x) > 0 or (y3 - y) * (y4 - y) > 0:
            result = np.array([np.nan, np.nan])
    return result


def irradiate(position: np.ndarray, angle: float) -> np.ndarray:
    """
        args:
            position: どこから
            angle: どの向きに
        return: p1が起点でp2を通る半直線
    """
    p1: np.ndarray = position
    p2: np.ndarray = np.array([
        position[0] + np.cos(angle),
        position[1] + np.sin(angle)
    ])
    half_line: np.ndarray = np.array([p1, p2])
    return half_line


def receive(
        half_line: np.ndarray, segments: np.ndarray
) -> np.ndarray:
    x1, y1 = half_line[0]
    """最も近い壁の反射だけが見えるよね"""
    distances: np.ndarray = np.zeros(len(segments))
    results: np.ndarray = np.array([
        _reflect(half_line=half_line, segment=segment)
        for segment in segments
    ])

    for i, result in enumerate(results):
        _p1 = np.array(result)
        if not np.isnan(_p1).any():
            _p2 = np.array([x1, y1])
            distances[i] = np.linalg.norm(_p1 - _p2)
        else:
            distances[i] = np.inf
    i_nearest: int = int(np.argmin(distances))
    return results[i_nearest]
