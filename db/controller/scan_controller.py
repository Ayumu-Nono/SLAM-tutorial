from typing import List
import numpy as np

from model.scan import Scan
from db.interactor.scan_interactor import ScanInteractor
from .util.scan_util import transform_cartesian2mesh, transform_polar2cartesian


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
        cartesian_arr = transform_polar2cartesian(
            polar_arr=np.array(scan.data),
            self_position=self_position,
            self_angle=self_angle
        )
        return transform_cartesian2mesh(
            cartesian_arr=cartesian_arr, mesh_digit=mesh_digit,
            mesh_xs=mesh_xs, mesh_ys=mesh_ys
        )
    
    def get_2ndlatest_as_mesh(
        self, self_position: np.ndarray, self_angle: float,
        mesh_digit: int, mesh_xs: np.ndarray, mesh_ys: np.ndarray
    ) -> np.ndarray:
        scan = self.__scan_interactor.get_2ndlatest()
        cartesian_arr = transform_polar2cartesian(
            polar_arr=np.array(scan.data),
            self_position=self_position,
            self_angle=self_angle
        )
        return transform_cartesian2mesh(
            cartesian_arr=cartesian_arr, mesh_digit=mesh_digit,
            mesh_xs=mesh_xs, mesh_ys=mesh_ys
        )

    def get_latest_as_cartesian_arr(
        self, self_position: np.ndarray, self_angle: float
    ) -> np.ndarray:
        scan = self.__scan_interactor.get_latest()
        cartesian_arr = transform_polar2cartesian(
            polar_arr=np.array(scan.data),
            self_position=self_position,
            self_angle=self_angle
        )
        return cartesian_arr
