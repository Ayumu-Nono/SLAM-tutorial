import numpy as np


def transform_cartesian2mesh(
    cartesian_arr: np.ndarray, mesh_digit: int,
    mesh_xs: np.ndarray, mesh_ys: np.ndarray
) -> np.ndarray:
    _floor_cartesian_arr = np.floor(cartesian_arr * 10 ** mesh_digit)
    _floor_cartesian_arr *= 10 ** (-mesh_digit)
    floor_cartesian_arr: np.ndarray = np.unique(_floor_cartesian_arr, axis=0)
    floor_cartesian_arr = floor_cartesian_arr.round(decimals=mesh_digit)
    assert floor_cartesian_arr.shape[1] == 2, "2次元座標が崩れてる"
    mesh: np.ndarray = np.zeros((len(mesh_xs), len(mesh_ys)))
    # 範囲外を消す
    isin: np.ndarray = np.isin(floor_cartesian_arr[:, 0], mesh_xs) \
        == np.isin(floor_cartesian_arr[:, 1], mesh_xs)
    assert len(floor_cartesian_arr) == len(isin)
    ixs = np.array([np.argwhere(mesh_xs == p[0]) for p in floor_cartesian_arr[isin]])
    iys = np.array([np.argwhere(mesh_ys == p[1]) for p in floor_cartesian_arr[isin]])
    assert ixs.shape == iys.shape
    mesh[ixs, iys] = 1.0
    return mesh


def transform_polar2cartesian(
    polar_arr: np.ndarray, self_position: np.ndarray, self_angle: float
) -> np.ndarray:
    ds: np.ndarray = np.array(polar_arr)[:, 0]
    angles: np.ndarray = np.array(polar_arr)[:, 1]
    xs: np.ndarray = ds * np.cos(angles + self_angle) + self_position[0]
    ys: np.ndarray = ds * np.sin(angles + self_angle) + self_position[1]
    assert len(xs) == len(ys)
    cartesian_arr: np.ndarray = np.array([
        np.array([xs[i], ys[i]]) for i in range(len(xs))
    ])
    return cartesian_arr
