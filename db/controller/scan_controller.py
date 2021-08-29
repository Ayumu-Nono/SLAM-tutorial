from typing import List
import numpy as np

from model.scan import Scan
from db.interactor.scan_interactor import ScanInteractor


class ScanController:
    def __init__(self) -> None:
        self.__scan_interactor: ScanInteractor = ScanInteractor()

    def push_with_arr(self, data: np.ndarray) -> int:
        assert isinstance(data, np.ndarray)
        data_as_list: List[tuple] = [
            (row[0], row[1]) for row in data
        ]
        is_success: bool = self.__scan_interactor.push(
            scan=Scan(data=data_as_list)
        )
        assert is_success
        return self.__scan_interactor.get_len()

    def get_latest_as_polar_arr(self) -> np.ndarray:
        scan = self.__scan_interactor.get_latest()
        return np.array(scan.data)

    def get_latest_as_mesh(
        self, self_position: np.ndarray, self_angle: float,
        mesh_digit: int, mesh_xs: np.ndarray, mesh_ys: np.ndarray
    ) -> np.ndarray:
        scan = self.__scan_interactor.get_latest()
        ds: np.ndarray = np.array(scan.data)[:, 0]
        angles: np.ndarray = np.array(scan.data)[:, 1]
        xs: np.ndarray = ds * np.cos(angles + self_angle) + self_position[0]
        ys: np.ndarray = ds * np.sin(angles + self_angle) + self_position[1]
        assert len(xs) == len(ys)
        cartesian_arr: np.ndarray = np.array([
            np.array([xs[i], ys[i]]) for i in range(len(xs))
        ])
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

    def get_latest_as_cartesian_arr(
        self, self_position: np.ndarray, self_angle: float
    ) -> np.ndarray:
        scan = self.__scan_interactor.get_latest()
        ds: np.ndarray = np.array(scan.data)[:, 0]
        angles: np.ndarray = np.array(scan.data)[:, 1]
        xs: np.ndarray = ds * np.cos(angles + self_angle) + self_position[0]
        ys: np.ndarray = ds * np.sin(angles + self_angle) + self_position[1]
        assert len(xs) == len(ys)
        points: np.ndarray = np.array([
            np.array([xs[i], ys[i]]) for i in range(len(xs))
        ])
        return points
