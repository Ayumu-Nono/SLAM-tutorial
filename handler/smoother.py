import numpy as np
from copy import deepcopy

from db.controller.status_controller import StatusController
from db.controller.scan_controller import ScanController

from .util.smoother_util import calc_score

class Smoother:
    def __init__(
        self,
        pred_status_controller: StatusController,
        smtd_status_controller: StatusController,
        scan_controller: ScanController
    ) -> None:
        assert isinstance(pred_status_controller, StatusController)
        assert isinstance(smtd_status_controller, StatusController)
        assert isinstance(scan_controller, ScanController)
        self.__pred_status_controller: StatusController = pred_status_controller
        self.__smtd_status_controller: StatusController = smtd_status_controller
        self.__scan_controller: ScanController = scan_controller

    def set_initial_status(self, position: np.ndarray, angle: float) -> int:
        assert self.__smtd_status_controller.get_latest_tstep_as_int() == 0
        t: int = self.__smtd_status_controller.push_with_arr(position, angle)
        return t

    def smooth(
        self, mesh_digit: int, mesh_xs: np.ndarray, mesh_ys: np.ndarray,
        passing_rate: float, max_distance: float,
        position_vs_angle_cost_ratio: float,
        mesh_vs_status_cost_ratio: float
    ) -> int:
        _2ndlatest_position: np.ndarray = self.__smtd_status_controller.get_latest_position_as_arr()
        _2ndlatest_angle: float = self.__smtd_status_controller.get_latest_angle_as_float()
        pred_position: np.ndarray = self.__pred_status_controller.get_latest_position_as_arr()
        pred_angle: float = self.__pred_status_controller.get_latest_angle_as_float()
        ref_mesh: np.ndarray = self.__scan_controller.get_2ndlatest_as_mesh(
            self_position=_2ndlatest_position, self_angle=_2ndlatest_angle,
            mesh_digit=mesh_digit, mesh_xs=mesh_xs, mesh_ys=mesh_ys
        )
        smtd_position = deepcopy(pred_position)
        smtd_angle = deepcopy(pred_angle)
        mesh = self.__scan_controller.get_latest_as_mesh(
            self_position=smtd_position,
            self_angle=smtd_angle,
            mesh_digit=mesh_digit, mesh_xs=mesh_xs, mesh_ys=mesh_ys
        )
        score = calc_score(
            mesh=mesh,
            ref_mesh=ref_mesh,
            pred_position=pred_position, pred_angle=pred_angle,
            smtd_position=smtd_position, smtd_angle=smtd_angle,
            passing_rate=passing_rate, max_distance=max_distance,
            position_vs_angle_cost_ratio=position_vs_angle_cost_ratio,
            mesh_vs_status_cost_ratio=mesh_vs_status_cost_ratio
        )

        t: int = self.__smtd_status_controller.push_with_arr(pred_position, pred_angle)
        return t
